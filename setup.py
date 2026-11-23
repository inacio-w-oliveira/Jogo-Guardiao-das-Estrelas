
import os
import sys
import cx_Freeze

os.chdir(os.path.dirname(os.path.abspath(__file__)))

clicado_direto = len(sys.argv) == 1
if clicado_direto:
    sys.argv.append("build")

executaveis = [
    cx_Freeze.Executable(
        script="main.py",
        icon="bases/icone.ico",
        target_name="GuardiaoDasEstrelas.exe"
    )
]

try:
    cx_Freeze.setup(
        name="Guardiao das Estrelas",
        options={
            "build_exe": {
                "packages": ["pygame", "pyttsx3"],
                "include_files": ["bases", "Recursos"]
            }
        },
        executables=executaveis
    )
except Exception as erro:
    print("Erro ao gerar executavel:", erro)
    if clicado_direto:
        input("Pressione Enter para fechar...")

# python setup.py build
