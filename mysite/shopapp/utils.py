

def product_preview_directory_path(
        instance: "Product",
        filename: str
) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk, filename=filename
    )


def product_images_directory_path(
        instance: "ProductImage",
        filename: str
) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )