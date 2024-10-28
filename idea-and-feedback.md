## ROBOTICS PROJECT IDEA : 
For our project we have decided to build a recycling system. In this system the rubbish will be sorted out into different categories by robot arms and then the sorted rubbish will be loaded into rovers which will take the rubbish to designated areas - rovers will be able to detect obstacles, take themselves to docking pods in addition to being able to tell if bins are full.

Robot sorts out trash, recycling system + Robot sorts out blocks by colour, size…
Robot Types: Arm
Sensors: RGB Colour, Infrared (or any shape sensor), Contact, proximity
Actuators: Rotating Joints
Effectors: Grab
Robot takes  sorted trash away to specific area
Robot Types: Rover
Sensors: GPS, Vision, proximity, internal sensors
Actuators: Wheels
Effectors: Grab ?

Cattegories of rubbish:
Recycling; 
Glass ,red
Paper, yellow
Metal, blue
General Waste
Other

Example Scenarios:
Robot breaks/loses power, so takes itself to dock for repair. Another rover replaces it.
Robot finds the shortest path to the next available bin, navigating objects and layout of the area.
Bins empty on a schedule so different ones will be full at different times.
 
## FEEDBACK : 

That is a very interesting idea, but it may be too complex to attempt. First, I suggest starting only with the robot arms and making every object (rubbish) the same shape and size, they only differ by colour. The arm should then be able to identify these and reorganise them until objects of the same colour are all separated into their own pile. After this is working, you can introduce a wheeled robot that will transport the sorted rubbish to another area. Make these robots follow a line or predetermined path, do not worry about obstacle avoidance or battery at this point, leave those things to the end. You should make the robot arm move the rubbish into the wheeled robot. Depending on the model you use, this may not be viable due to the physics of the objects and the wheeled robot. In this case, implement something at the logical level that will keep track of the objects the wheeled robot is carrying, even if they are not visually displayed in the simulator.




