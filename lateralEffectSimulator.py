import numpy as np
import cv2
import matplotlib as plt
import matplotlib.pyplot as plt
def simulate_line_scan_lateral(image, max_lateral_displacement, tilt_angle_profile=None, freq_Hz=1, speedkmh = 90, freq_per_row = 1):
    # Get image dimensions
    image_height, width, channels = image.shape
    # create sine graph with magnitude of max_lateral_displacement and frequency of freq_Hz

    #convert displacement in mm to displacement in pixels
    fov_in_mm = 1.5488
    pixels_displaced = int(max_lateral_displacement/(fov_in_mm))
    #Create x values --Need an x value for each camera trigger
    acquisition_rate = int(speedkmh*1000/3600/(fov_in_mm*10**-3)) #Hz
    x = np.linspace(0,1,acquisition_rate) #split 1 second for sample size  of acquisition rate
    #Find period for sine wave based on input freq_Hz
    b=2*np.pi*freq_Hz
    lateral_displacements = []
    #Create lateral displacement values following sine curve
    pixel_displacements = []
    if tilt_angle_profile=='sinusoid':
        for i in x:
            #displacement in mm for graph
            lateral_displacements.append(max_lateral_displacement*np.sin(b*i))
            #displacement in pixels for showing image distortion
            pixel_displacements.append(pixels_displaced*np.sin(b*i))
    elif tilt_angle_profile=='bump':
        x=np.linspace(0, image_height)
        for i in x:
                lateral_displacements.append(max_lateral_displacement/(i**2+1))
                pixel_displacements.append(pixels_displaced/(i**2+1))
    #plot graph
    fig, axs = plt.subplots(1,2)
    #plot graph of pixel displacement per trigger over the acquisition rate of one image on the left
    trigger_no = []
    pixel_displacements_in_one_image = pixel_displacements[:image_height]

    if tilt_angle_profile=='sinusoid':
        for i in range(image_height):
            pixel_displacements.append(pixels_displaced*np.sin(b*i))
            trigger_no.append(i)
        axs[0].plot(trigger_no, pixel_displacements_in_one_image)
    elif tilt_angle_profile=='bump':
        axs[0].plot(x, pixel_displacements)
    axs[0].set_title('Number of pixels shifted laterally each trigger over the capture of 1 image. Frequency = '+str(freq_Hz)+'Hz')
    axs[0].set_xlabel('Camera trigger')
    axs[0].set_ylabel('Pixels shifted laterally')
    #plot graph of mm lateral displacement in one second on the right
    axs[1].plot(x, lateral_displacements)
    axs[1].set_title('Lateral displacement in mm of line scan camera in 1 second when travelling at '+str(speedkmh)+'km/h')
    axs[1].set_xlabel('Seconds')
    axs[1].set_ylabel('Lateral displacement in mm')
    plt.show()
    
    # Create an empty array for the output image
    output_image = np.zeros((image_height, width+2*pixels_displaced, channels), dtype=np.uint8) #need to specify dtype otherwise the resulting image will look overexposed
    # in the new output image, each row of pixels is shifted to the right by the corresponding value in pixel_displacements
    for y in range(image_height):
        #shift the row of pixels to the right by the displacement in pixel_displacements
        for x in range(width):
            lateral_shift = int(pixel_displacements[y])
            if x+pixel_displacements[y] < width:
                output_image[y,x] = image[y,x+lateral_shift]
            else:
                output_image[y,x] = 0 #fill in with black if the pixel is out of range
    # Display the original and output images
    #reverse rgb to bgr for output image in cv2
    cv2.imshow('Original Image', image)
    cv2.imshow('Output Image', output_image)
    print(output_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return output_image
#running the function
image_path = 'effects-of-train-dynamics-on-camera-analysis/darren_images/14-03-18-AS_P2_IL_mp4-0003_jpg.rf.ffcb62d56e02ebd3a9159461bab4d285.jpg'  # Replace with your image path
image = cv2.imread(image_path)
max_lateral_displacement = 140 #mm
tilt_angle_profile = 'sinusoid'
freq_hz = 5
simulate_line_scan_lateral(image, max_lateral_displacement, tilt_angle_profile, freq_hz)
