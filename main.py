# Módulo: main.py
# Responsável por inicializar o controlador e a visualização

from controllers.restaurant_controller import RestaurantController
from views.restaurant_view import RestaurantView


def main():
    controller = RestaurantController()
    view = RestaurantView(controller)

    print(f"\nBem-vindo ao {controller.restaurante}")

    while True:
        view.display_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            view.cadastrar_garcom()
        elif opcao == "2":
            view.cadastrar_produto()
        elif opcao == "3":
            view.abrir_pedido()
        elif opcao == "4":
            view.mostrar_garcons()
        elif opcao == "5":
            view.mostrar_pedidos()
        elif opcao == "6":
            print("\nEncerrando o sistema. Até logo!")
            controller.close()
            break
        else:
            print("\nOpção inválida. Tente novamente.")


if __name__ == "__main__":
    main()

