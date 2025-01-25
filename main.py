# Importation du module partie1 depuis le dossier scripts
import scripts.partie1  # Assurez-vous que 'partie1.py' se trouve dans le dossier 'scripts'


def main():
    # Appel de la fonction d'initialisation de la simulation depuis partie1.py
    scripts.partie1.init_simulation()

    # Lancer la simulation depuis partie1.py
    scripts.partie1.run_simulation()


if __name__ == "__main__":
    main()
