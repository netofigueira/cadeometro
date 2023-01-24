import scrapy

class VivaRealSpider(scrapy.Spider):
    name = "viva_real"
    start_urls = [
        'https://www.vivareal.com.br/aluguel/sp/'
    ]

    def parse(self, response):
        for property in response.css('div.property-card'):
            yield {
                'title': property.css('h2.property-card__title span::text').get(),
                'address': property.css('div.property-card__address span::text').get(),
                'price': property.css('div.property-card__price span::text').get(),
                'area': property.css('div.property-card__specs-item span.property-card__specs-item-value::text')[0].get(),
                'bedrooms': property.css('div.property-card__specs-item span.property-card__specs-item-value::text')[1].get(),
                'bathrooms': property.css('div.property-card__specs-item span.property-card__specs-item-value::text')[2].get(),
                'parking': property.css('div.property-card__specs-item span.property-card__specs-item-value::text')[3].get(),
            }
