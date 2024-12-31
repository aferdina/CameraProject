# First Camera Project on Raspberry Pi

## Setup Raspberry Pi

### Install pyenv on Raspberry Pi

1. **Update and install dependencies**:
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev \
    liblzma-dev python-openssl git
    sudo apt install -y python3-picamera2 --no-install-recommends
    ```

2. **Install `pyenv`**:
    ```bash
    curl https://pyenv.run | bash
    ```

3. **Add `pyenv` to your shell startup file**:
    ```bash
    echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    ```

4. **Restart your shell**:

    ```bash
    exec $SHELL
    ```

5. **Verify the installation**:

    ```bash
    pyenv --version
    ```

### Create SSH key to connect to GitHub on Raspberry Pi

1. **Download git if not done**:

    ```bash
    sudo apt install git
    ```

2. **Generate the SSH key**:

    ```bash
    ssh-keygen -t ed25519 -C "your_email@example.com"
    ```

3. **Start the SSH agent**:

    ```bash
    eval "$(ssh-agent -s)"
    ```

4. **Add the SSH key to the SSH agent**:

    ```bash
    ssh-add ~/.ssh/id_ed25519
    ```

5. **Copy the SSH key to your clipboard**:

    ```bash
    cat ~/.ssh/id_ed25519.pub
    ```

6. **Add the SSH key to your GitHub account**:
    - Go to GitHub and navigate to **Settings** > **SSH and GPG keys** > **New SSH key**.
    - Paste the copied SSH key into the "Key" field and give it a title.

### Install Poetry on Raspberry Pi

1. **Install Poetry**:

    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

2. **Add Poetry to your PATH**:

    ```bash
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

3. **Verify the installation**:

    ```bash
    poetry --version
    ```
