builder_image := "hyprland-builder"
artifacts_dir := "artifacts"
default_chroot := "fedora-43-x86_64"
all_chroots := "fedora-43-x86_64 fedora-44-x86_64 fedora-rawhide-x86_64"

# dependency layers
layer0 := "hyprutils hyprwayland-scanner hyprland-protocols glaze awww"
layer1 := "hyprlang aquamarine hyprgraphics hyprpicker hyprpolkitagent hyprwire"
layer2 := "hyprcursor hypridle hyprlock hyprsunset xdg-desktop-portal-hyprland hyprtoolkit"
layer3 := "hyprland-guiutils hyprland"

packages := layer0 + " " + layer1 + " " + layer2 + " " + layer3

default:
    @just --list

# Prepare builder image
prepare:
    podman build -t {{builder_image}} -f Containerfile .

# Refresh local repo metadata for a chroot (indexes RPMs from previous layers)
_update-repo chroot:
    @mkdir -p {{artifacts_dir}}/{{chroot}}
    @chmod 777 {{artifacts_dir}}/{{chroot}}
    @podman run --rm --privileged --userns=keep-id \
        --security-opt label=disable \
        -v {{justfile_directory()}}:/src \
        {{builder_image}} \
        createrepo_c {{artifacts_dir}}/{{chroot}}

# Build a single package (assumes repo metadata is current)
_build-pkg package chroot:
    @podman unshare rm -rf {{artifacts_dir}}/{{chroot}}/{{package}}

    @mkdir -p {{artifacts_dir}}/{{chroot}} sources
    @chmod 777 {{artifacts_dir}}/{{chroot}} sources

    @podman run --rm --privileged --userns=keep-id \
        --security-opt label=disable \
        -v {{justfile_directory()}}:/src \
        {{builder_image}} \
        bash -c " \
            set +e; \
            ( \
                set -e; \
                REPO_DEF=\$(printf '[local-deps]\nname=Local\nbaseurl=file:///src/{{artifacts_dir}}/{{chroot}}\ngpgcheck=0\n'); \
                find {{package}} -maxdepth 1 -type f ! -name '*.spec' -exec cp {} sources/ \\;; \
                spectool -g -C sources {{package}}/{{package}}.spec; \
                mock -r {{chroot}} \
                    --buildsrpm \
                    --enable-network \
                    --spec {{package}}/{{package}}.spec \
                    --sources sources \
                    --resultdir {{artifacts_dir}}/{{chroot}}/{{package}}; \
                SRPM=\$(find {{artifacts_dir}}/{{chroot}}/{{package}} -name '*.src.rpm'); \
                mock -r {{chroot}} \
                    --rebuild \$SRPM \
                    --resultdir {{artifacts_dir}}/{{chroot}}/{{package}} \
                    --addrepo=\"\$REPO_DEF\" \
            ); \
            EXIT_CODE=\$?; \
            if [ \$EXIT_CODE -ne 0 ]; then echo 'Build failed!'; fi; \
            exit \$EXIT_CODE" || true

    @echo "fixing permissions..."
    @podman unshare chown -R 0:0 {{artifacts_dir}}/{{chroot}}/{{package}} sources

    @ls {{artifacts_dir}}/{{chroot}}/{{package}}/*.rpm 2>/dev/null | grep -qv '\.src\.rpm$' || (echo "No binary RPMs found, build failed." && exit 1)

# Build a single package for a given mock chroot
mock-build package chroot=default_chroot:
    just _update-repo {{chroot}}
    just _build-pkg {{package}} {{chroot}}

# Build all packages for a single chroot (parallel within layers, sequential between layers)
mock-build-all chroot=default_chroot:
    #!/usr/bin/env bash
    trap 'kill 0 2>/dev/null; exit 1' INT TERM

    FAIL_LOG="{{artifacts_dir}}/{{chroot}}/.failures"
    rm -f "$FAIL_LOG"
    all_failures=()

    build_layer() {
        local layer_name=$1; shift
        echo "=== $layer_name: $* ==="
        just _update-repo "{{chroot}}"
        local pids=()
        local pkgs=("$@")
        for pkg in "${pkgs[@]}"; do
            just _build-pkg "$pkg" "{{chroot}}" &
            pids+=($!)
        done
        local layer_failed=0
        for i in "${!pids[@]}"; do
            if ! wait "${pids[$i]}"; then
                all_failures+=("${pkgs[$i]}")
                layer_failed=1
            fi
        done
        if [ $layer_failed -ne 0 ]; then
            echo "=== $layer_name FAILED ==="
            return 1
        fi
        echo "=== $layer_name done ==="
    }

    stopped_at=""
    build_layer "Layer 0" {{layer0}} || stopped_at="Layer 0"
    [ -z "$stopped_at" ] && { build_layer "Layer 1" {{layer1}} || stopped_at="Layer 1"; }
    [ -z "$stopped_at" ] && { build_layer "Layer 2" {{layer2}} || stopped_at="Layer 2"; }
    [ -z "$stopped_at" ] && { build_layer "Layer 3" {{layer3}} || stopped_at="Layer 3"; }

    if [ ${#all_failures[@]} -gt 0 ]; then
        printf '%s\n' "${all_failures[@]}" > "$FAIL_LOG"
        echo ""
        echo "FAILED [{{chroot}}]: ${all_failures[*]} (stopped at $stopped_at)"
        exit 1
    fi

# Build all packages for all chroots in parallel
mock-build-all-chroots +CHROOTS=all_chroots:
    #!/usr/bin/env bash
    trap 'kill 0 2>/dev/null; exit 1' INT TERM
    chroots=({{CHROOTS}})
    pids=()
    for chroot in "${chroots[@]}"; do
        echo "Starting builds for $chroot..."
        just mock-build-all "$chroot" &
        pids+=($!)
    done
    for pid in "${pids[@]}"; do
        wait "$pid" || true
    done

    echo ""
    echo "=============================="
    echo "        BUILD SUMMARY"
    echo "=============================="
    any_failed=0
    for chroot in "${chroots[@]}"; do
        FAIL_LOG="{{artifacts_dir}}/$chroot/.failures"
        if [ -f "$FAIL_LOG" ]; then
            any_failed=1
            failed_pkgs=$(tr '\n' ' ' < "$FAIL_LOG")
            echo "  FAIL  $chroot: $failed_pkgs"
        else
            echo "    OK  $chroot"
        fi
    done
    echo "=============================="
    if [ $any_failed -ne 0 ]; then
        exit 1
    fi

# Clean artifacts directory
clean:
    podman unshare rm -rf {{artifacts_dir}} sources

# Open a shell in the builder container
shell:
    podman run --rm --privileged --userns=keep-id --security-opt label=disable -it -v {{justfile_directory()}}:/src {{builder_image}} bash

# Rebuild single package in Copr
copr-build package:
    copr build-package nikromen/hyprland --name {{package}}

# Rebuild all packages in Copr (parallel within layers via batches, layers sequenced via --after-build-id)
copr-build-all:
    #!/usr/bin/env bash
    set -e

    echo "Checking Copr packages..."
    REMOTE=$(copr list-package-names nikromen/hyprland)
    MISSING=()
    for pkg in {{packages}}; do
        echo "$REMOTE" | grep -qx "$pkg" || MISSING+=("$pkg")
    done
    if [ ${#MISSING[@]} -gt 0 ]; then
        echo "ERROR: packages not in Copr: ${MISSING[*]}"
        exit 1
    fi

    PREV_BATCH_ID=""

    copr_build_layer() {
        local layer_name=$1; shift
        local batch_id=""
        echo "=== $layer_name: $* ==="
        for pkg in "$@"; do
            if [ -z "$batch_id" ]; then
                if [ -z "$PREV_BATCH_ID" ]; then
                    OUTPUT=$(copr build-package nikromen/hyprland --name "$pkg" --nowait)
                else
                    OUTPUT=$(copr build-package nikromen/hyprland --name "$pkg" --nowait --after-build-id "$PREV_BATCH_ID")
                fi
                batch_id=$(echo "$OUTPUT" | grep -oP 'Created builds: \K\d+')
            else
                OUTPUT=$(copr build-package nikromen/hyprland --name "$pkg" --nowait --with-build-id "$batch_id")
            fi
            BID=$(echo "$OUTPUT" | grep -oP 'Created builds: \K\d+')
            echo "  Queued $pkg (build ID: $BID)"
        done
        PREV_BATCH_ID="$batch_id"
    }

    copr_build_layer "Layer 0" {{layer0}}
    copr_build_layer "Layer 1" {{layer1}}
    copr_build_layer "Layer 2" {{layer2}}
    copr_build_layer "Layer 3" {{layer3}}

    echo "All builds queued! https://copr.fedorainfracloud.org/coprs/nikromen/hyprland/builds/"

# Check for outdated packages (compares upstream tags with spec versions)
check-versions:
    #!/usr/bin/env bash
    echo "Checking package versions..."
    echo ""
    for pkg in {{packages}}; do
        SPEC="$pkg/$pkg.spec"
        [ ! -f "$SPEC" ] && continue

        SPEC_VER=$(grep -m1 '^Version:' "$SPEC" | awk '{print $2}')
        UPSTREAM_URL=$(grep -m1 '^%global forgeurl' "$SPEC" | awk '{print $3}')
        if [ -z "$UPSTREAM_URL" ]; then
            echo "$pkg: no forgeurl found"
            continue
        fi

        LATEST_VER=$(curl -sL "$UPSTREAM_URL/releases" | grep -m1 'href.*releases/tag' | grep -oP 'releases/tag/v?\K[0-9.]+' | head -1)

        if [ -z "$LATEST_VER" ]; then
            LATEST_VER=$(curl -sL "$UPSTREAM_URL/tags" | grep -m1 'href.*releases/tag' | grep -oP 'releases/tag/v?\K[0-9.]+' | head -1)
        fi

        if [ -z "$LATEST_VER" ]; then
            echo "$pkg: could not fetch upstream version"
            continue
        fi

        if [ "$SPEC_VER" != "$LATEST_VER" ]; then
            echo "$pkg: $SPEC_VER -> $LATEST_VER (UPDATE AVAILABLE)"
        else
            echo "$pkg: $SPEC_VER (up to date)"
        fi
    done
