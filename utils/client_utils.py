def cliente_existe(servidor, cliente_id):
    """Verifica si un cliente con el ID dado existe en el servidor."""
    try:
        cliente_id = int(cliente_id)
    except (ValueError, TypeError):
        return False
    return servidor.obtener_cliente_por_id(cliente_id) is not None
