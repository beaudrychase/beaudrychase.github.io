# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

ARG USER=vscode
ARG DEBIAN_FRONTEND=noninteractive
RUN usermod -s /usr/bin/bash ${USER}

# VARIANT can be either 'hugo' for the standard version or 'hugo_extended' for the extended version.
ARG VARIANT=hugo_extended
# VERSION can be either 'latest' or a specific version number
ARG VERSION=latest

# Download Hugo
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
RUN case "${VERSION}" in \
    latest) \
    VERSION=$(wget --output-document - \
    --quiet \
    https://api.github.com/repos/gohugoio/hugo/releases/latest | grep "tag_name" | awk '{print substr($2, 3, length($2)-4)}') \
    export VERSION ;;\
    esac && \
    echo "${VERSION}" && \
    case $(uname -m) in \
    aarch64) \
    ARCH=ARM64 \
    export ARCH ;; \
    *) \
    ARCH=64bit \
    export ARCH ;; \
    esac && \
    echo "${ARCH}" && \
    wget -O "${VERSION}.tar.gz" "https://github.com/gohugoio/hugo/releases/download/v${VERSION}/${VARIANT}_${VERSION}_Linux-${ARCH}.tar.gz" && \
    tar xf "${VERSION}.tar.gz" && \
    mv hugo /usr/bin/hugo

# Hugo dev server port
EXPOSE 1313


USER ${USER}
ARG HOME=/home/${USER}
WORKDIR ${HOME}

ARG PNPM_HOME=${HOME}/.local/share/pnpm
ENV PATH="${PNPM_HOME}:$PATH"
RUN <<EOT
    wget -qO- https://get.pnpm.io/install.sh | ENV="${HOME}/.bashrc" SHELL=/bin/bash sh -
    pnpm env use -g lts
EOT

# ARG OHMYZSH_THEME=${OHMYZSH_HOME}/custom/themes
# RUN <<EOT
#     git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${OHMYZSH_THEME}/powerlevel10k
#     sed -i 's|ZSH_THEME="devcontainers"|ZSH_THEME="powerlevel10k/powerlevel10k"|g' .zshrc
#     echo 'POWERLEVEL9K_DISABLE_CONFIGURATION_WIZARD=true' >> .zshrc
# EOT