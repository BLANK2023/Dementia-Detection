import React, { useState } from "react";
import "./App.css";

function ImageUpload() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [prediction, setPrediction] = useState(null);
    const [loading, setLoading] = useState(false);
    const [imagePreview, setImagePreview] = useState(null);
    const [showResult, setShowResult] = useState(false);

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            setSelectedFile(file);
            setImagePreview(URL.createObjectURL(file));
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;
        setLoading(true);
        setShowResult(false);
        const formData = new FormData();
        formData.append("file", selectedFile);
    
        try {
            const response = await fetch("http://127.0.0.1:8000/predict", {
                method: "POST",
                body: formData,
            });
    
            const data = await response.json();
            console.log("API Response:", data);  // Debugging
            setPrediction(data);
            setShowResult(true);
        } catch (error) {
            console.error("Error:", error);
            setPrediction({ category: "Error", description: "", advice: "" });
        } finally {
            setLoading(false);
        }
    };
    

    return (
        <div className={`container ${showResult ? "result-stage" : "upload-stage"}`}>
            <div className="left-panel">
                <h2>Upload MRI Image</h2>
                <input type="file" onChange={handleFileChange} />
                <button className="check-result"  onClick={handleUpload}>Check Result</button>
                {imagePreview && (
                    <div className="image-preview">
                        <h3>Uploaded Image:</h3>
                        <img src={imagePreview} alt="Uploaded" />
                    </div>
                )}
                
            </div>
            <div className="right-panel">
                {loading && <p>Loading...</p>}
                {showResult && prediction && (
                    <div className="result-content">
                        <h2>{prediction.category}</h2>
                        <p><strong>Description:</strong> {prediction.description}</p>

                        {prediction.characteristics && prediction.characteristics.length > 0 && (
                            <>
                                <h3>Characteristics</h3>
                                <ul>
                                    {prediction.characteristics.map((item, index) => (
                                        <li key={index}>{item}</li>
                                    ))}
                                </ul>
                            </>
                        )}

                        {prediction.advice && prediction.advice.length > 0 && (
                            <>
                                <h3>Advice</h3>
                                <ul>
                                    {prediction.advice.map((item, index) => (
                                        <li key={index}>{item}</li>
                                    ))}
                                </ul>
                            </>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
}

export default ImageUpload;
