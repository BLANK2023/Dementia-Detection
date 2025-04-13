# Dementia-Detection

MODEL : 
	"p.ipynb" is the main file. 
    	First Run All the Jupyter notebook will which Download the dataset from kaggle, 
    	also It wiil create the models namely :
	
    1.baseliine_cnn.keras
		
	2.augmented_cnn.keras
		
	3.transfer_learning_resnet50.keras
		
	4.dementia_model.h5



FastAPI Backend (Python) : 

Run this in Jupyter Notebook or Command Prompt:
	  
	      pip install fastapi uvicorn pillow torch torchvision
	
after installation run
	  
	      uvicorn backend:app --reload


Frontend : 

Create a React App (If Not Initialized)
	
Run the following command to set up a React project:
	     
	     npx create-react-app frontend
	
	
Reelocate "ImageUpload.jsx" and "app.css" file to "frontend/src/component/"

create "component" folder if not present

Navigate to the new React project and start the server:
    
    cd frontend
    npm start
