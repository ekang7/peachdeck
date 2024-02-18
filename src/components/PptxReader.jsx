import React, { useState } from 'react';
import JSZip from 'jszip'; // Import JSZip library
import axios from 'axios';

const PptxReader = () => {
  const [file, setFile] = useState(null);
  const [text, setText] = useState([]);
  const [topic, setTopic] = useState('');

  function getTextFromNodes(node, tagName, namespaceURI, isExtractingSlideNotes = false) {
    if(!isExtractingSlideNotes){
      let currSlideText = {}
      let slideBulletPoints = []
      const textNodes = node.getElementsByTagNameNS(namespaceURI, tagName);
      if(textNodes.length == 0) return currSlideText;
      currSlideText["title"] = textNodes[0].textContent.trim();
      for (let i = 1; i < textNodes.length; i++) {
        slideBulletPoints.push(textNodes[i].textContent.trim());
      }
      currSlideText["bullet_points"] = slideBulletPoints;
      return currSlideText;
    } else{
      const textNodes = node.getElementsByTagNameNS(namespaceURI, tagName);
      if(textNodes.length == 0) return [];
      let currSpeakerNotes = [];
      for (let i = 0; i < textNodes.length; i++) {
        currSpeakerNotes.push(textNodes[i].textContent.trim());
      }
      return currSpeakerNotes;
    }
  }

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
  };

  const handleFileUpload = async (e) => {
    if (!file) return;

    e.preventDefault();

    const reader = new FileReader();
    reader.onload = async (event) => {
      const arrayBuffer = event.target.result;
      const zip = await JSZip.loadAsync(arrayBuffer);

      const aNamespace = "http://schemas.openxmlformats.org/drawingml/2006/main";

      let allSlidesText = []
      let slideIndex = 1;
      while (true) {
        const slideFile = zip.file(`ppt/slides/slide${slideIndex}.xml`);
        const notesFile = zip.file(`ppt/notesSlides/notesSlide${slideIndex}.xml`);
        
        if (!slideFile) break;
        
        const slideXmlStr = await slideFile.async('text');
        const notesXmlStr = await notesFile.async('text');
        
        const parser = new DOMParser();
        const slidesXmlDoc = parser.parseFromString(slideXmlStr, 'application/xml');
        const notesXmlDoc = parser.parseFromString(notesXmlStr, 'application/xml');
        
        let currSlideDict = getTextFromNodes(slidesXmlDoc, "t", aNamespace);
        currSlideDict["speaker_notes"] = getTextFromNodes(notesXmlDoc, "t", aNamespace);
        allSlidesText.push(currSlideDict);
        
        slideIndex++;
      }
      
      setText(allSlidesText);
      setTopic(allSlidesText[0]["title"])
      console.log(text);
      console.log(topic);
      try {
        // Send data to Flask server
        const response = await axios.post('http://localhost:5000/api/endpoint', {'topic' : topic, 'slides_data': allSlidesText});
        console.log('Response from server:', response.data);
        // Handle response as needed
      } catch (error) {
        console.error('Error sending data:', error);
        // Handle error
      }
      return allSlidesText;
    };
    reader.readAsArrayBuffer(file);
  };
  
  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleFileUpload}>Upload and Read PPTX</button>
    </div>
  );
};

export default PptxReader;