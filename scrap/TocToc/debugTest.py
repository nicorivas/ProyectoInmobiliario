from scrapTocToc import house_data, base_building_search, building_data, apartment_data, apartment_value_data

#url = 'https://www.toctoc.com/search/index2/?dormitorios=0&banos=0&superficieDesde=0&superficieHasta=0&precioDesde=0&precioHasta=0&moneda=UF&tipoArriendo=false&tipoVentaUsado=true&tipoVentaNuevo=true&tipoUltimasVentas=false&casaDepto=undefined&ordenarPorMoneda=UFCLP&ordenarDesc=false&ordernarPorFechaPublicacion=false&ordernarPorSuperficie=false&ordernarPorPrecio=false&pagina=1&textoBusqueda=&tipoVista=lista&viewport=-33.55089671454338%2C-70.6644412867289%2C-33.36701030778827%2C-70.49003332774453&comuna=&region=&atributos=&idle=true&zoom=12&buscando=false&vuelveBuscar=false&dibujaPoligono=false&resetMapa=false&animacion=false&idZonaHomogenea=0&esPrimeraBusqueda=false'
#base_building_search(url)

#url = 'https://www.toctoc.com/propiedades/compranuevo/departamento/providencia/edificio-don-salvador/475345'
#print(building_data(url, 'prueba'))

#url = 'https://www.toctoc.com/propiedades/compranuevo/departamento/providencia/parque-roman-diaz/522247'
#print(apartment_data(url, 'prueba'))


url = 'https://www.toctoc.com/propiedades/compranuevo/departamento/providencia/bilbao-blanco/429500'
user = 'the_big_lebowsky@hotmail.com'
password = 'toctocpass123'
print(apartment_value_data(url, user, password))

