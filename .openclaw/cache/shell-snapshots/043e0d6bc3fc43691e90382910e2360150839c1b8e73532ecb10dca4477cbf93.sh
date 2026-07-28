# OpenClaw exec shell snapshot. Generated; do not edit.
if [ -n "${BASH_VERSION:-}" ]; then shopt -s expand_aliases 2>/dev/null || true; fi
unalias -a 2>/dev/null || true
command_not_found_handle () 
{ 
    if [ -x /usr/lib/command-not-found ]; then
        /usr/lib/command-not-found -- "$1";
        return $?;
    else
        if [ -x /usr/share/command-not-found/command-not-found ]; then
            /usr/share/command-not-found/command-not-found -- "$1";
            return $?;
        else
            printf "%s: command not found\n" "$1" 1>&2;
            return 127;
        fi;
    fi
}
export PATH='/usr/bin:/usr/bin:/bin:/root/.vscode-server/data/User/globalStorage/github.copilot-chat/debugCommand:/root/.vscode-server/data/User/globalStorage/github.copilot-chat/copilotCli:/root/.vscode-server/cli/servers/Stable-1b6a188127eeaf9194f945eb6eb89a657e93c54c/server/bin/remote-cli:/usr/local/sbin:/usr/local/bin:/usr/sbin:/sbin:/usr/games:/usr/local/games:/snap/bin'