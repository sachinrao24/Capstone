import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import "./App.css";
import FrontPage from "./Pages/FrontPage/frontPage";
import ExercisePage from './Pages/ExercisePage/exercisePage';
import MediaPipePage from "./Pages/MediaPipePage/mediaPipePage";
import NavBar from "./Components/NavBar/navBar";
import Footer from "./Components/Footer/footer";

const App = () => {
  return (
    <Router>
      <NavBar />
      <Routes>
        <Route exact path="/" element={<FrontPage />} />
        <Route exact path="/exercises" element={<ExercisePage />} />
        <Route exact path="/check_form" element={<MediaPipePage />} />
      </Routes>
      <Footer />
    </Router>
  );
};

export default App;

// import React, { useRef, useState } from 'react';
// import Webcam from 'react-webcam';
// import axios from 'axios';

// function App() {
//   const webcamRef = useRef(null);
//   const [processing, setProcessing] = useState(false);

//   const captureImage = async () => {
//     setProcessing(true);
//     const imageSrc = webcamRef.current.getScreenshot();
//     const response = await axios.post('/check_form', { imageData: imageSrc });
//     console.log(response.data.message);
//     setProcessing(false);
//   };

//   return (
//     <div className="App">
//       <Webcam
//         audio={false}
//         ref={webcamRef}
//         screenshotFormat="image/jpeg"
//       />
//       <button onClick={captureImage} disabled={processing}>Process Image</button>
//       {processing && <p>Processing image...</p>}
//     </div>
//   );
// }

// export default App;

