# ADGM-Compliant Corporate Agent with Document Intelligence



# Overview
This task implements an agent that will assist in reviewing, validating, and helping users prepare documentation for business incorporation and compliance within the Abu Dhabi Global Market (ADGM) jurisdiction.




### Setup instructions
```bash
# Clone the repository
git clone <repository-url>

# Install dependencies
pip install -r requirements.txt

# Create a .env file and the paste the api key there
GOOGLE_API_KEY=<your-api-key>

# Run the streamlit app
streamlit run app.py


```



## Project Structure

```
├── data                    # Contains the data for RAG
├── main.py                 # Builds the AI Agent
├── lancedb                 # vector db
├── app.py                  # Streamlit app
├── utils.py                # Utility functions
├── requirements.txt        # Requirements

```

## Example Documents (screenshot)

# Before review:
<img width="492" height="647" alt="image" src="https://github.com/user-attachments/assets/c4fddcea-43a6-4d63-bbc1-832db14f495a" />



# After review:
<img width="536" height="717" alt="image" src="https://github.com/user-attachments/assets/249bdf7f-c37a-410b-b2a3-6c5cda642481" />
