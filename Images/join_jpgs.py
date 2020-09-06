from PIL import Image
import sys


def open_image(filename):
    filename = filename.strip().replace('\\', '')

    image = Image.open(filename)

    return image


if __name__ == '__main__':
    outfile = f"{sys.argv[1].strip().replace('\\', '').split('.')[0]}.pdf"
    og_image = open_image(sys.argv[2])

    im_list = []
    for file in sys.argv[3:]:
        new_image = open_image(file)
        im_list.append(new_image)

    og_image.save(outfile, "PDF", resolution=500.0,
                  save_all=True, append_images=im_list)
    print(f"Saved to {outfile}")
