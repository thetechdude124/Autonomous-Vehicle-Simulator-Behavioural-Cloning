# 🌐 Simulating Autonomous Vehicles using Behavioural Cloning

https://www.youtube.com/watch?v=HDSw95Cojp8

🚗 Nearly **1.2 million** people die each year due to car accidents - due to careless errors, impaired driving, and reckless behaviour. 

⚙️**Autonomous Vehicles** serve as a potential solution to this problem. Leveraging the high processing speeds of moden computers, such vehicles can make **split-second** desicions with high accuracies.

💡I decided to **implement one myself!** As someone who's HUGELY passionate about Artifical Intelligence, **I began wondering if I could create a self-driving vehicle using traditional deep learning techniques.**

# 🤔 How it works

I found Udacity's Autonomous Vehicle Simulator and decided to **build a Convolutional Neural Network** (CNN) to drive the car automatically around a track! This project uses the philosophy of **behavioural cloning** - attempting to mimic human behaviour using Artificial Intelligence - to enable self-driving functionality. 

After hours of training, I arrived at a model that was actually able to accomplish this. Regardless, the CNN still isn't purpose - I've made some updates to these files as I train better models with lower loss values.

After training is done, the project uses **a server-client model** using Python anf Flask to actually _drive_ the vehicle. Basically:

1.  **The simulator** (client) sends **images** every second to the API/Server
2.  **The Flaks API/Server** activates the model and runs the images through the CNN
3.  **The CNN** then outputs a **steering angle** and sends it back to the server
4.  **The server then sends the steering angle to the client** - the car can now drive!

_NOTE: For more detail, including mockups and detailed analyses, check out the video above!_

All in all, this project was a FANTASTIC accelerator for both my deep learning and programming abilities. Feel free to check it all out!

Regards,

Aditya Dewan
