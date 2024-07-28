import './App.css'
import { useEffect, useState } from 'react'

function App() {

  const API_URL = 'http://localhost:8000/receive-data';

  const [data, setData] = useState('');

  // Function to save data to local storage
  const saveToLocalStorage = (value) => {
    localStorage.setItem('myDataKey', value);
  };

  // Function to get data from local storage
  const getFromLocalStorage = () => {
    const storedData = localStorage.getItem('myDataKey');
    if (storedData) {
      setData(storedData);
    } else {
      console.log('No data found in local storage');
    }
  };

  // Function to send data to FastAPI backend
  const sendDataToFastAPI = async () => {
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'usersession': data
        },
        //body: JSON.stringify({ data }),
        body: JSON.stringify({"message": 'data send'}),
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Response from FastAPI:', result);
      } else {
        console.error('Failed to send data to FastAPI:', response.status);
      }
    } catch (error) {
      console.error('Error sending data to FastAPI:', error);
    }
  };

  useEffect(() => {
    getFromLocalStorage();
    sendDataToFastAPI();
  }, []);

  const usersession = JSON.stringify({
    "name": "sarabjeet",
    "linux": "Archlinux",
    "kernel": "zen kernel"
  })

  return (
    <>
    <div>
      <h1>Local Storage and FastAPI</h1>
      <button onClick={() => saveToLocalStorage(usersession)}>
        Save Data to Local Storage
      </button>
      <button onClick={getFromLocalStorage}>
        Get Data from Local Storage
      </button>
      <button onClick={sendDataToFastAPI}>
        Send Data to FastAPI
      </button>
      <p>Data from Local Storage: {data}</p>
    </div>
    </>
  )
}

export default App
