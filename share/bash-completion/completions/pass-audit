# pass-audit completion file for bash

PASSWORD_STORE_EXTENSION_COMMANDS+=(audit)

__password_store_extension_complete_audit() {
	local args=(-f --filename -h --help -q --quiet -v --verbose -V --version)
	COMPREPLY+=($(compgen -W "${args[*]}" -- ${cur}))
	_pass_complete_entries
	compopt -o nospace
}
