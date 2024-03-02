### What it does
PeachDeck turns PowerPoint slides into AI-generated video presentations. It doesn't just summarize the slides, but it uses RAG LLM model to expand upon the lecture and teach the nitty gritty of that professors didn't mention in only a matter of minutes. It can be applied for consultants, training videos, teachers, and students.

### Inspiration
What happens when you miss a class and all you have is a deck of lecture slides filled with bullet point content and no context? One of our members often missed classes because of illness/other commitments, and they fell behind because lecture slides often provide insufficient context. What if there was a way for them to catch up on lectures easily? Using RAG LLM, however, we can turn disjointed lecture slides into a cohesive video presentation with immaculate generative voiceovers, allowing students to pick up missed concepts in a short amount of time. But our AI-powered journey doesn't stop there. We're not just filling gaps; we're amplifying the learning experience. Instructors often can't dive deep into every concept in class, leaving students curious about what wasn't covered. Our AI agent steps in, providing in-depth explanations for concepts left untouched in class. It's not just about catching up; it's about delving into the intricacies of each subject. The use case is not confined to schools alone – it can help with any kind of training and educational videos. It reduces the time it takes for instructors to prepare online courses, and also eliminates the need for extensive manual video production, making corporate training more budget-friendly. We hope to democratize access to high-quality content, reaching learners around the world and contributing to a more equitable education landscape.

### How we built it
Use Bun to create the React app and install all needed packages
Used PredictionGuard AI from Intel to create a safe RAG LLM model (AI Agent) for university textbooks
Used Python for data cleaning
We found open-source textbooks with free for commercial use licenses which we then embedded as vectors with multimodal CLIP
We used the open-source en_core_web_md model from spaCy to classify what subject a lecture belonged to and thus indexed to the appropriate vector embedding space
Used ElevenLabs for audio generation with multiple generative AI voices
Used React for the frontend
Used Figma for prototyping: https://www.figma.com/file/TPEmQIIjMAyELI5sIkzbeP/Trees!?type=design&node-id=93%3A26453&mode=design&t=ruoBvc9hY4f9oCzR-1
Used Flask for the backend server
Used Spire to convert pptx slides to images and add audio over them
Challenges we ran into
We ran into many challenges when merging our front-end and back-end programs together, as the merge involved combining a variety of difficult conversions, such as extracting text from powerpoints, integrating text with audio, and converting audio to video. The last one took an especially long time to resolve as generating video files are often quite tedious. Asking prompts - after 4 hours of playing around, we discovered that LLMs did better with less information than with more counterintuitively

### Accomplishments that we're proud of
We are especially proud of the level of the pipeline we've managed to execute, using a plethora of different algorithms to make something extraordinarily useful for the education industry. End-to-end design of the web app on Figma after many iterations; we want to create something that is aesthetically pleasing and intuitive to use I have never built a RAG LLM model before and was surprised to learn how cool and fun it was, especially with mentors from Intel!

### What we learned
Getting advice from experts in the field of what you're looking into is extremely helpful. By talking to experienced engineers and thinkers early on in our journey, we were able to dream big and accomplish tasks at a more monumental level.

### What's next for
We hope that the product would evolve into something that allows users to edit the AI-generated content and customize it more directly. Users can review generated scripts from slides first, and regenerate if they are not satisfied. They can also edit the video directly within the platform, and use the chatbot for further assistance. Ability to add AI-generated avatars (we already have voices and the ability to change between them but do not have a clear way to do this on our current interface).

In the future, we also want to add translations, so it enables people who are not fluent in English learn from slides in their native language! We hope that one day everyone can attend any lecture in the world!

### Built With
agent
ai
api
bun
css
elevenlabs
figma
flask
html
intel
javascript
langchain
llm
neurachat
numpy
open-source
pandas
python
rag
react
spacey
spire
