builder_image := "hyprland-builder"
target := "fedora-43-x86_64"
artifacts_dir := "artifacts"

default:
    @just --list

# Prepare builder image
prepare:
    podman build -t {{builder_image}} -f Containerfile .

# Build a single package
mock-build package:
    @podman unshare rm -rf {{artifacts_dir}}/{{package}}

    @mkdir -p {{artifacts_dir}} sources
    @chmod 777 {{artifacts_dir}} sources

    @podman run --rm --privileged --userns=keep-id \
        --security-opt label=disable \
        -v {{justfile_directory()}}:/src \
        {{builder_image}} \
        bash -c " \
            set +e; \
            ( \
                set -e; \
                createrepo_c {{artifacts_dir}} > /dev/null; \
                REPO_DEF=\$(printf '[local-deps]\nname=Local\nbaseurl=file:///src/{{artifacts_dir}}\ngpgcheck=0\n'); \
                spectool -g -C sources {{package}}/{{package}}.spec; \
                mock -r {{target}} \
                    --buildsrpm \
                    --enable-network \
                    --spec {{package}}/{{package}}.spec \
                    --sources sources \
                    --resultdir {{artifacts_dir}}/{{package}}; \
                SRPM=\$(find {{artifacts_dir}}/{{package}} -name '*.src.rpm'); \
                mock -r {{target}} \
                    --rebuild \$SRPM \
                    --resultdir {{artifacts_dir}}/{{package}} \
                    --addrepo=\"\$REPO_DEF\" \
            ); \
            EXIT_CODE=\$?; \
            if [ \$EXIT_CODE -ne 0 ]; then echo 'Build failed!'; fi; \
            exit \$EXIT_CODE" || true

    @echo "fixing permissions..."
    @podman unshare chown -R 0:0 {{artifacts_dir}} sources

    @ls {{artifacts_dir}}/{{package}}/*.rpm >/dev/null 2>&1 || (echo "No RPMs found, build failed." && exit 1)

# Package build order (ORDER MATTERS! Some packages depend on others)
packages := "hyprutils hyprlang hyprwayland-scanner aquamarine hyprgraphics hyprlock hyprland-protocols hyprtoolkit hyprland-guiutils hypridle hyprcursor hyprsunset xdg-desktop-portal-hyprland hyprpicker glaze hyprland hyprpolkitagent awww"

# Build the entire ecosystem in the correct order
mock-build-all:
    #!/usr/bin/env bash
    for pkg in {{packages}}; do
        just mock-build "$pkg"
    done

# Clean artifacts directory
clean:
    podman unshare rm -rf {{artifacts_dir}} sources

# Open a shell in the builder container
shell:
    podman run --rm --privileged --userns=keep-id --security-opt label=disable -it -v {{justfile_directory()}}:/src {{builder_image}} bash

# Rebuild single package in Copr
copr-build package:
    copr build-package nikromen/hyprland --name {{package}}

# Rebuild multiple packages in Copr sequentially
copr-build-batch +PACKAGES:
    #!/usr/bin/env bash
    set -e
    PREV_ID=""
    for pkg in {{PACKAGES}}; do
        if [ -z "$PREV_ID" ]; then
            OUTPUT=$(copr build-package nikromen/hyprland --name "$pkg" --nowait)
        else
            OUTPUT=$(copr build-package nikromen/hyprland --name "$pkg" --nowait --after-build-id "$PREV_ID")
        fi
        PREV_ID=$(echo "$OUTPUT" | grep -oP 'Created builds: \K\d+')
        echo "Queued $pkg (build ID: $PREV_ID)"
    done
    echo "All builds queued. Monitor at: https://copr.fedorainfracloud.org/coprs/nikromen/hyprland/builds/"

# Rebuild all packages in Copr in correct dependency order
copr-build-all:
    just copr-build-batch {{packages}}

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
