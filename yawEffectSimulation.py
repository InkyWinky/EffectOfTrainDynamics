import numpy as np
import cv2
import matplotlib as plt
import matplotlib.pyplot as plt
image_path = 'input_image.jpg'  # Replace with your image path
image = cv2.imread(image_path)
def simulate_line_scan_yaw(image, tilt_angle, frequency=1, tilt_angle_profile=None, sin_freq_factor=1, speedkmh = 90):
    #Frequency is how often the tilt occurs, every ___ row of pixels set to 1 for occuring every row
    #Tilt_angle_profile is either None or 'sinusoid' 
    #Sin_freq_factor is a factor that reduces/increases frequency of the sinusoid
    #speedkms is the speed of the train in km per hour
    # Convert tilt angle to radians
    angle_rad = np.deg2rad(tilt_angle)
    
    # Get image dimensions
    height, width, channels = image.shape
    #print(height, width)
    # Create an empty array for the output image
    output_image = np.zeros_like(image)
    pivot = width/2 #middle of image (pivot point for tilt)
    # Calculate the shift per line based on the tilt angle
    gradient = np.tan(angle_rad)
    #print(gradient)
    c=0 #vertical offset
    x_vals = np.linspace(0, height, height+1)
    if tilt_angle_profile=='sinusoid':
        tilt_angles_sin=[]
        #print(x_vals)
        for i in x_vals:
            tilt_angles_sin.append(np.deg2rad(tilt_angle)*np.sin(sin_freq_factor*i))
        fov_in_mm = 1.5488
        acquisition_rate = int(speedkmh*1000/3600/(fov_in_mm*10**-3)) #Hz
        period_of_trigger_sin = 2*np.pi/sin_freq_factor
        periods_per_second = acquisition_rate/period_of_trigger_sin
        period_of_sin_in_sec = 1/periods_per_second
        tilt_angles_sin_per_second=[]
        seconds = np.linspace(0,1,acquisition_rate)
        b = (2*np.pi)/period_of_sin_in_sec
        for i in seconds:
            tilt_angles_sin_per_second.append(np.deg2rad(tilt_angle)*np.sin(b*i))
        #make 2 subplots
        fig, axs = plt.subplots(1,2)
        
        # plot graph of tilt angles per trigger on the left
        axs[0].plot(x_vals, np.rad2deg(tilt_angles_sin))
        axs[0].set_title('Yaw of line scan camera at each trigger. Frequency factor = '+str(sin_freq_factor))
        axs[0].set_xlabel('Camera trigger')
        axs[0].set_ylabel('Yaw of camera (degrees)')
        #plot graph of tilt angles per second on the right
        axs[1].plot(seconds, np.rad2deg(tilt_angles_sin_per_second))
        axs[1].set_title('Yaw of line scan camera at each second when travelling at '+str(speedkms)+'km/h')
        axs[1].set_xlabel('Seconds')
        axs[1].set_ylabel('Yaw of camera (degrees)')
        plt.show()

       
    for y in range(height): #for height of original image
        if tilt_angle_profile=='sinusoid':
            used_grad = np.tan(tilt_angles_sin[y])#
        else:
            used_grad = gradient
        for x in range(width):

            y_old = int(used_grad*(x-pivot)+c) #part of original image that line covers
            # Copy the pixel from the original image to the new position
            #print(y_old)
            if y%frequency !=0:
                #Keep original row
                output_image[y,x] = image[y,x]
            elif y_old>=height or y_old<0:
                output_image[y, x] = [0,0,0] #black if no data
            
            else:
                output_image[y, x] = image[y_old, x]
        c+=1
            
    return output_image, x_vals, tilt_angles_sin
tilt_angle = 0.1  # plus minus tilt angle in degrees
output_image, x_vals, tilt_angles_sin = simulate_line_scan_yaw(image, tilt_angle, 1, 'sinusoid', 0.001)
cv2.imwrite('output_image.jpg', output_image)
cv2.imshow('Output Image', output_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#plot 4*8 grid of images and plots where the sin_freq_factor increases horizontally and the tilt angle increases vertically
# sin_freq_factors = [0.01,0.05,0.1,0.5,1]
# tilt_angles = [0.1,0.5,1,2,5]
# fig, axs = plt.subplots(4, 5, figsize=(10,10))   
# #decrease font size of titles 
# plt.rc('axes', titlesize=8)
# #remove axis numbers
# plt.setp(axs, xticks=[], yticks=[])
# for i in range(4):
#     for j in range(5):
#         output_image, x_vals, tilt_angles_sin = simulate_line_scan(image, tilt_angles[i],sin_freq_factor=sin_freq_factors[j], tilt_angle_profile='sinusoid')
#         axs[i, j].imshow(output_image[...,::-1])
#         axs[i, j].set_title('Tilt angle: ±'+str(tilt_angles[i])+'° Sin freq factor: '+str(sin_freq_factors[j]))
#         # axs[i,j+1].plot(x_vals, np.rad2deg(tilt_angles_sin))
# plt.show()
