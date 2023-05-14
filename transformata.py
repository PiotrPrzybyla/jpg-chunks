from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def display_spectrum(image_path):
    # Wczytaj obraz i przekształć go na skale szarości
    img = Image.open(image_path).convert('L')

    # Przekształć obraz na tablicę numpy
    img_data = np.asarray(img)

    # Przeprowadź transformację Fouriera
    fft_result = np.fft.fft2(img_data)

    # Przesuń zerową częstotliwość do środka
    fft_shifted = np.fft.fftshift(fft_result)

    # Oblicz widmo mocy
    spectrum = np.abs(fft_shifted)

    # Wyświetl widmo
    plt.imshow(np.log1p(spectrum), cmap='gray')
    plt.title('Spectrum')
    plt.show()


def test_fft(image_path):
    img = Image.open(image_path).convert('L')
    img_data = np.asarray(img)

    # Przeprowadź transformację Fouriera
    fft_result = np.fft.fft2(img_data)

    # Przeprowadź odwrotną transformację Fouriera
    ifft_result = np.fft.ifft2(fft_result)

    # Oblicz różnicę między oryginalnym obrazem a obrazem po transformacji i odwrotnej transformacji
    difference = np.abs(img_data - ifft_result)

    print(f"Maximum difference: {np.max(difference)}")


def transform(name):
    display_spectrum(name)
    test_fft(name)