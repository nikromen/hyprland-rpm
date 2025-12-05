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

# Build the entire ecosystem in the correct order
mock-build-all:
    # ORDER MATTERS! Some packages depend on others
    just mock-build hyprutils
    just mock-build hyprlang
    just mock-build hyprwayland-scanner
    just mock-build aquamarine
    just mock-build hyprgraphics
    just mock-build hyprlock
    just mock-build hyprland-protocols
    just mock-build hypridle
    just mock-build hyprcursor
    just mock-build hyprsunset
    just mock-build xdg-desktop-portal-hyprland
    just mock-build hyprpicker
    just mock-build glaze
    just mock-build hyprland
    just mock-build hyprpolkitagent
    # unrelated packages, but I use them
    just mock-build awwww

# Clean artifacts directory
clean:
    podman unshare rm -rf {{artifacts_dir}} sources

# Open a shell in the builder container
shell:
    podman run --rm --privileged --userns=keep-id --security-opt label=disable -it -v {{justfile_directory()}}:/src {{builder_image}} bash
