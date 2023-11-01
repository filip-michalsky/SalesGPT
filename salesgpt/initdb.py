import os
from tortoise import Tortoise, run_async
from salesgpt.models import ProductCatalog
from dotenv import load_dotenv

load_dotenv()  # loads .env file


async def init_db():

    await Tortoise.init(
        db_url=os.environ.get('DB_URL'),
        modules={'models': ['models']},
    )
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()

    await Tortoise.init(
        db_url=os.environ.get('DB_URL'),
        modules={'models': ['__main__']},
    )

    await ProductCatalog.create(
        name='Luxury Cloud-Comfort Memory Foam Mattress',
        type='Twin, Queen, King',
        price=999,
        desc='''Experience the epitome of opulence with our Luxury Cloud-Comfort Memory Foam Mattress. Designed with an innovative, temperature-sensitive memory foam layer, this mattress embraces your body shape, offering personalized support and unparalleled comfort. The mattress is completed with a high-density foam base that ensures longevity, maintaining its form and resilience for years. With the incorporation of cooling gel-infused particles, it regulates your body temperature throughout the night, providing a perfect cool slumbering environment. The breathable, hypoallergenic cover, exquisitely embroidered with silver threads, not only adds a touch of elegance to your bedroom but also keeps allergens at bay. For a restful night and a refreshed morning, invest in the Luxury Cloud-Comfort Memory Foam Mattress.'''
    )
    await ProductCatalog.create(
        name='Classic Harmony Spring Mattress',
        type='Queen, King',
        price=1299,
        desc='''A perfect blend of traditional craftsmanship and modern comfort, the Classic Harmony Spring Mattress is designed to give you restful, uninterrupted sleep. It features a robust inner spring construction, complemented by layers of plush padding that offers the perfect balance of support and comfort. The quilted top layer is soft to the touch, adding an extra level of luxury to your sleeping experience. Reinforced edges prevent sagging, ensuring durability and a consistent sleeping surface, while the natural cotton cover wicks away moisture, keeping you dry and comfortable throughout the night. The Classic Harmony Spring Mattress is a timeless choice for those who appreciate the perfect fusion of support and plush comfort.'''
    )
    await ProductCatalog.create(
        name='EcoGreen Hybrid Latex Mattress',
        type='Twin, Full',
        price=1599,
        desc='''The EcoGreen Hybrid Latex Mattress is a testament to sustainable luxury. Made from 100% natural latex harvested from eco-friendly plantations, this mattress offers a responsive, bouncy feel combined with the benefits of pressure relief. It is layered over a core of individually pocketed coils, ensuring minimal motion transfer, perfect for those sharing their bed. The mattress is wrapped in a certified organic cotton cover, offering a soft, breathable surface that enhances your comfort. Furthermore, the natural antimicrobial and hypoallergenic properties of latex make this mattress a great choice for allergy sufferers. Embrace a green lifestyle without compromising on comfort with the EcoGreen Hybrid Latex Mattress.'''
    )
    await ProductCatalog.create(
        name='Plush Serenity Bamboo Mattress',
        type='King',
        price=2599,
        desc='''The Plush Serenity Bamboo Mattress takes the concept of sleep to new heights of comfort and environmental responsibility. The mattress features a layer of plush, adaptive foam that molds to your body's unique shape, providing tailored support for each sleeper. Underneath, a base of high-resilience support foam adds longevity and prevents sagging. The crowning glory of this mattress is its bamboo-infused top layer - this sustainable material is not only gentle on the planet, but also creates a remarkably soft, cool sleeping surface. Bamboo's natural breathability and moisture-wicking properties make it excellent for temperature regulation, helping to keep you cool and dry all night long. Encased in a silky, removable bamboo cover that's easy to clean and maintain, the Plush Serenity Bamboo Mattress offers a luxurious and eco-friendly sleeping experience.'''
    )


if __name__ == "__main__":
    run_async(init_db())
