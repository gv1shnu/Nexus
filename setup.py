# Refer note.txt

from cx_Freeze import setup, Executable

base = None

executables = [
    Executable("app.py", base=base),
]

build_exe_options = {
    "includes": [
    ],
    "include_files": [
        ("templates", "templates"),
        ("static", "static"),
        ("src", "src"),
        ("scr", "scr"),
        ("cdr", "cdr"),
    ],
}

setup(
    name="SearchNexus",
    description="Search Nexus Application",
    options={
        "build_exe": build_exe_options
    },
    executables=executables
)
