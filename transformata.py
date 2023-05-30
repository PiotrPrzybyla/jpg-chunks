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

    print(f"Difference: {np.max(difference)}")


def display_spectrum_and_phase(image_path):
    # Load the image and convert to grayscale
    img = Image.open(image_path).convert('L')

    # Transform the image into a numpy array
    img_data = np.asarray(img)

    # Perform Fourier Transform
    fft_result = np.fft.fft2(img_data)

    # Shift the zero frequency to the center
    fft_shifted = np.fft.fftshift(fft_result)

    # Compute power spectrum and phase
    spectrum = np.abs(fft_shifted)
    phase = np.angle(fft_shifted)

    # Display power spectrum
    plt.figure(figsize=(10, 4))
    plt.subplot(121)
    plt.imshow(np.log1p(spectrum), cmap='gray')
    plt.title('Spectrum')

    # Display phase
    plt.subplot(122)
    plt.imshow(phase, cmap='gray')
    plt.title('Phase')
    plt.show()

def verify_transform(image_path):
    img = Image.open(image_path).convert('L')
    img_data = np.asarray(img)

    # Perform Fourier Transform
    fft_result = np.fft.fft2(img_data)

    # Shift the zero frequency to the center
    fft_shifted = np.fft.fftshift(fft_result)

    # Shift back the zero frequency to the top left corner
    fft_unshifted = np.fft.ifftshift(fft_shifted)

    # Perform inverse Fourier Transform
    ifft_result = np.fft.ifft2(fft_unshifted)

    # Compute difference between original image and image after transform and inverse transform
    difference = np.abs(img_data - ifft_result)

    # Verify that the maximum difference is below a threshold (for example, 1e-6)
    assert np.max(difference) < 1e-6, "Transform and inverse transform did not recover the original image"

    # Compute power spectrum and phase
    spectrum = np.abs(fft_shifted)
    phase = np.angle(fft_shifted)

    # Verify power spectrum and phase against expected values
    # ...

def transform(name):
    # display_spectrum(name)
    # test_fft(name)
    display_spectrum_and_phase(name)