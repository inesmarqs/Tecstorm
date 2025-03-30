
import json
from sqlalchemy.orm import Session
from db_session import get_db
from database.models import Product, Ingredient, NutricionalInformation, Category
from database.commands_database import add_product, add_category, add_product_populate, add_ingredient, add_nutricional_info
from sqlalchemy.exc import IntegrityError

db: Session = next(get_db())


barra1 = "5449000054227"
barra2 = "5449000133328"
barra3 = "5411188110835"
barra4 = "8434165466395"
barra5 = "8436048963861"

bebidas_e_garrafeira = db.query(Category).filter(Category.name == "bebidas-e-garrafeira").first()
bolacha = db.query(Category).filter(Category.name == "bolacha").first()
laticinios_e_ovos = db.query(Category).filter(Category.name == "laticinios-e-ovos").first()

cola = add_product_populate(db, barra1, "Coca-Cola",
                            "https://www.continente.pt/produto/refrigerante-com-gas-cola-coca-cola-2391674.html",
                            "Coca-Cola Sabor Original é uma bebida refrescante com o sabor inconfundível da sua Coca-Cola de sempre, desde 1886. A garrafa de 1 litro é o formato perfeito para as refeições em família ou com os amigos. A sua Coca-Cola ainda mais refrescante, com muito mais gelo e uma rodela de lima ou limão.",
                            "Coca-Cola", 1.5, "2391674", "https://www.continente.pt/dw/image/v2/BDVS_PRD/on/demandware.static/-/Sites-col-master-catalog/default/dwc8cd5a78/images/col/239/2391674-hero.png?sw=2000&sh=2000",
                            None, bebidas_e_garrafeira.id)


cola_zero = add_product_populate(db, barra2, "Coca-Cola Zero",
                                 "https://www.continente.pt/produto/refrigerante-com-gas-cola-zero-coca-cola-3788322.html",
                                 None,
                                 "Coca-Cola", 1.35, "3788322", "https://www.continente.pt/dw/image/v2/BDVS_PRD/on/demandware.static/-/Sites-col-master-catalog/default/dwa642bbdb/images/col/378/3788322-hero-.png.jpg?sw=2000&sh=2000",
                                 None, bebidas_e_garrafeira.id)
alpro_amendoa = add_product_populate(db, barra3, "Bebida Vegetal de Amêndoa Torrada",
                                     "https://www.continente.pt/produto/bebida-vegetal-de-amendoa-torrada-alpro-5254417.html",
                                     "Benefícios: - 100% vegetal;  Naturalmente baixa em gorduras saturadas; Fonte de vitamina E; Fácil de digerir porque é naturalmente isenta de lactose e glúten.",
                                     "Alpro", 1.89, "5254417", "https://www.continente.pt/dw/image/v2/BDVS_PRD/on/demandware.static/-/Sites-col-master-catalog/default/dwd1807752/images/col/525/5254417-cima.jpg?sw=2000&sh=2000",
                                     None, laticinios_e_ovos.id)

chocoguay = add_product_populate(db, barra4, "Bolachas com Recheio de Leite e Cacau Tosta Rica Choco Guay",
                                 "https://www.continente.pt/produto/bolachas-com-recheio-de-leite-e-cacau-tosta-rica-choco-guay-cuetara-2384858.html",
                                 "Tosta Rica é uma bolacha nutritiva, com cereais, vitaminas, ferro e cálcio. Chocoguay é a Tosta Rica recheada com delicioso creme de leite e cacau, em embalagens individuais, práticas para levar para todo o lado. Tosta Rica alimenta a imaginação.",
                                 "Cuétara", 2.29, "2384858", "https://www.continente.pt/dw/image/v2/BDVS_PRD/on/demandware.static/-/Sites-col-master-catalog/default/dw92df63b4/images/col/238/2384858-direito.jpg?sw=2000&sh=2000",
                                 None, bolacha.id)
chocoleche = add_product_populate(db, barra5, "Bolachas Dinossauros Chocolate de Leite",
                                  "https://www.continente.pt/produto/bolachas-dinossauros-chocolate-de-leite-artiach-7801288.html",
                                  None,
                                  "Artiach", 3.39, "7801288", "https://www.continente.pt/dw/image/v2/BDVS_PRD/on/demandware.static/-/Sites-col-master-catalog/default/dwd232a1aa/images/col/780/7801288-direito.jpg?sw=2000&sh=2000",
                                  None, bolacha.id)

add_nutricional_info(db, 180, 42, 0,0,10.6,10.6,0,0,0, cola)
add_nutricional_info(db, 0.9, 0.2, 0,0,0,0,0,0,0.02, cola_zero)
add_nutricional_info(db, 108, 26, 1.1,0.1,3.1,3.1,0.3,0.4,0.14, alpro_amendoa)
add_nutricional_info(db, 2050, 488, 20,9,70,31,2.4,5.9,0.49, chocoguay)
add_nutricional_info(db, 2066, 493, 22, 6.5, 67, 29, 2.4, 5.5, 0.932, chocoleche)
add_ingredient(db, cola, "agua")
add_ingredient(db, cola, "acucar")
add_ingredient(db, cola, "dioxido de carbono")
add_ingredient(db, cola, "corante caramelo E-150d")
add_ingredient(db, cola, "acidificante acido fosforico")
add_ingredient(db, cola, "aromas naturais")
add_ingredient(db, cola, "aroma cafeina")
add_ingredient(db, cola_zero, "agua")
add_ingredient(db, cola_zero, "acucar")
add_ingredient(db, cola_zero, "dioxido de carbono")
add_ingredient(db, cola_zero, "corante caramelo E-150d")
add_ingredient(db, cola_zero, "acidificante acido fosforico")
add_ingredient(db, cola_zero, "aromas naturais")
add_ingredient(db, cola_zero, "aroma cafeina")
add_ingredient(db, cola_zero, "ciclamato de sodio")
add_ingredient(db, cola_zero, "acessulfame K")
add_ingredient(db, cola_zero, "aspartame")
add_ingredient(db, cola_zero, "glicosídeos de esteviol produzidos enzimaticamente")
add_ingredient(db, cola_zero, "regulador de acidez")
add_ingredient(db, cola_zero, "citratos de sódio")
add_ingredient(db, alpro_amendoa, "agua")
add_ingredient(db, alpro_amendoa, "acucar")
add_ingredient(db, alpro_amendoa, "amendoa")
add_ingredient(db, alpro_amendoa, "sal marina")
add_ingredient(db, alpro_amendoa, "vestigios de frutos de casca rija(sem amendoim)")
add_ingredient(db, alpro_amendoa, "sem gluten")
add_ingredient(db, alpro_amendoa, "sem lactose")
add_ingredient(db, chocoguay, "farinha de trigo")
add_ingredient(db, chocoguay, "acucar")
add_ingredient(db, chocoguay, "clara de ovos")
add_ingredient(db, chocoguay, "lactose")
add_ingredient(db, chocoguay, "gaseificantes")
add_ingredient(db, chocoguay, "soja")
add_ingredient(db, chocoguay, "mostarda")
add_ingredient(db, chocoguay, "vestigios de frutos de casca rija")
add_ingredient(db, chocoleche, "cereais")
add_ingredient(db, chocoleche, "acucar")
add_ingredient(db, chocoleche, "lactose")
add_ingredient(db, chocoleche, "mostarda")
add_ingredient(db, chocoleche, "soja")
add_ingredient(db, chocoleche, "ovo")


