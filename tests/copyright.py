url = "http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/"


two_fp_with_invalid_field = """
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/

Files: foobar.foo
Copyright: Foo Bar <foo@bar.com>
Licens: Beerware


Files: sara.sa
Copyright: Sara Sa <sara@sa.com>
License: Vaporware

""".splitlines(True)


invalid_single_line_values = """
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
 or http://debian.org/copyright-format/1.0/
""".splitlines(True)


invalid_header = """
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Upstream-Name: SOFTware
Upstream-Contact: John Doe <john.doe@example.com>
Source: http://www.example.com/software/project
Files: *
License: GPL-2
""".splitlines(True)


invalid_file = """
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
Files: *
License: GPL-2
""".splitlines(True)


invalid_standalone = """
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
License: GPL-2
Comment: Some comments
""".splitlines(True)


two_headers = """
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/

Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
""".splitlines(True)


header = """
Format: http://www.debian.org/doc/packaging-manuals/copyright-format/1.0/
""".splitlines(True)


two_fp_without_header = """
Files: foobar.foo
Copyright: Foo Bar <foo@bar.com>
License: Beerware


Files: sara.sa
Copyright: Sara Sa <sara@sa.com>
License: Vaporware

""".splitlines(True)


repeated_fields = """
Files: foobar.foo
Files: foobar.foo
Copyright: Foo Bar <foo@bar.com>
License: Beerware
""".splitlines(True)
