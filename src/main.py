from recomendador import RecomendadorLibros


def main():

    print("===================================")
    print(" RECOMENDADOR DE LIBROS CON IA ")
    print("===================================")

    # Crear recomendador
    recomendador = RecomendadorLibros()

    while True:

        print("\nEscribe lo que buscas.")
        print("Ejemplo:")
        print("'Quiero un libro de fantasia con romance'")
        print("Escribe 'salir' para terminar.\n")

        consulta = input("Tu búsqueda: ")

        if consulta.lower() == "salir":
            print("\nPrograma finalizado.")
            break

        try:

            resultados = recomendador.recomendar(consulta)

            print("\n===== LIBROS RECOMENDADOS =====\n")

            for i, (_, libro) in enumerate(resultados.iterrows(), start=1):

                print(f"{i}. {libro['title']}")
                print(f"   Autor: {libro['authors']}")
                print(f"   Categoría: {libro['categories']}")
                print(f"   Páginas: {libro['num_pages']}")
                print(f"   Rating: {libro['average_rating']}")
                print()

        except Exception as e:

            print("\nOcurrió un error:")
            print(e)


if __name__ == "__main__":
    main()