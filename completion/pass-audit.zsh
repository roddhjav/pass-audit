#compdef pass-audit
#description Audit your password repository

_pass-audit () {
	_arguments : \
        {-f,--filename}'[check only passwords with this filename]' \
		{-h,--help}'[display help information]' \
		{-V,--version}'[display version information]' \
		{-q,--quiet}'[be quiet]' \
		{-v,--verbose}'[be verbose]'
	_pass_complete_entries_with_subdirs
}

_pass-audit "$@"
