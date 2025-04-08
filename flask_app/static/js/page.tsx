// Note: The "use client" directive is specific to frameworks like Next.js and might not be needed.
// Note: Imports for UI components (@/components/ui/button) and AI SDK (@ai-sdk/openai)
// assume you have a similar setup in your JavaScript environment or have replaced them
// with appropriate alternatives. The AI generation part might need a backend API.

import React, { useState, useRef, useEffect } from "react";
import { Mic, MicOff, Square } from "lucide-react"; // Assuming lucide-react is available
// Adjust this import based on your component library setup
// import { Button } from "@/components/ui/button"; // Original TSX import
// Example: Assuming a simple Button component or placeholder
const Button = ({ children, ...props }) => <button {...props}>{children}</button>;

// Note: The AI generation part likely requires a backend API call in a browser environment.
// The original code uses an AI SDK directly, which might not work client-side without adjustments.
// import { generateText } from "ai"; // Original import
// import { openai } from "@ai-sdk/openai"; // Original import

// Placeholder for the AI function - replace with your API call logic
async function callJarvisAPI() {
    // Example: Replace with fetch('/api/jarvis', { method: 'POST', ... })
    console.log("Calling placeholder AI function...");
    await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate network delay
    return { text: "System status: All systems nominal. Ready for instructions." }; // Example response
}


export default function Home() {
    const [isActive, setIsActive] = useState(false);
    const [isMuted, setIsMuted] = useState(false);
    const [response, setResponse] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const audioRef = useRef(null);
    const canvasRef = useRef(null);
    const animationRef = useRef(null);

    useEffect(() => {
        // Ensure this runs only in the browser
        if (typeof window !== "undefined") {
            audioRef.current = new Audio("/jarvis-sound.mp3"); // Ensure this path is correct [cite: 1]
            if (audioRef.current) {
                audioRef.current.loop = true; [cite: 1]
            }
        }
    }, []);

    useEffect(() => {
        if (audioRef.current) {
            audioRef.current.muted = isMuted; [cite: 3]
        }
    }, [isMuted]);

    useEffect(() => {
        if (isActive && canvasRef.current) {
            startAnimation(); [cite: 3]
        } else {
            stopAnimation(); [cite: 3]
        }

        // Cleanup function
        return () => {
            stopAnimation(); [cite: 4]
        };
    }, [isActive]);

    const startAnimation = () => {
        if (!canvasRef.current) return; [cite: 4]

        const canvas = canvasRef.current;
        const ctx = canvas.getContext("2d"); [cite: 4]
        if (!ctx) return; [cite: 4]

        const width = canvas.width; [cite: 4]
        const height = canvas.height; [cite: 4]
        const centerY = height / 2; [cite: 4]
        // const waveCount = 3; // Original - not used in loop logic below
        // const waveWidth = width / waveCount; // Original - not used

        let offset = 0; [cite: 4]

        const animate = () => {
            ctx.clearRect(0, 0, width, height); [cite: 5]
            ctx.beginPath(); [cite: 5]

            // Draw the wave [cite: 5]
            for (let x = 0; x < width; x++) {
                const y = centerY + Math.sin(x / 20 + offset) * 20; [cite: 5]
                if (x === 0) {
                    ctx.moveTo(x, y); [cite: 5]
                } else {
                    ctx.lineTo(x, y); [cite: 6]
                }
            }

            ctx.strokeStyle = "rgba(59, 130, 246, 0.8)"; [cite: 6]
            ctx.lineWidth = 4; [cite: 6]
            ctx.stroke(); [cite: 6]

            offset += 0.1; [cite: 6]
            animationRef.current = requestAnimationFrame(animate); [cite: 6]
        };

        animate(); [cite: 6]
    };

    const stopAnimation = () => {
        if (animationRef.current !== null) {
            cancelAnimationFrame(animationRef.current); [cite: 6]
            animationRef.current = null; [cite: 7]

            if (canvasRef.current) {
                const canvas = canvasRef.current; [cite: 7]
                const ctx = canvas.getContext("2d"); [cite: 7]
                if (ctx) {
                    ctx.clearRect(0, 0, canvas.width, canvas.height); [cite: 7]
                }
            }
        }
    };

    const handleActivate = async () => {
        setIsActive(true); [cite: 7]
        setIsLoading(true); [cite: 7]

        if (audioRef.current && !isMuted) {
            audioRef.current.play(); [cite: 8]
        }

        try {
            // Replace direct AI SDK call with API call
            // const { text } = await generateText({
            //   model: openai("gpt-4o"),
            //   prompt: "Respond as Jarvis from Iron Man. Give a brief status update on the system.", [cite: 9]
            //   system: "You are Jarvis, the AI assistant from Iron Man. Be concise, helpful, and slightly formal.", [cite: 10]
            // });
            const { text } = await callJarvisAPI(); // Use the placeholder/API call function

            setResponse(text); [cite: 10]
        } catch (error) {
            console.error("Error generating response:", error); [cite: 10]
            setResponse("I'm sorry, I encountered an error processing your request."); [cite: 10]
        } finally {
            setIsLoading(false); [cite: 10]
        }
    };

    const handleStop = () => {
        setIsActive(false); [cite: 10]
        if (audioRef.current) {
            audioRef.current.pause(); [cite: 10]
            audioRef.current.currentTime = 0; [cite: 10]
        }
    };

    const toggleMute = () => {
        setIsMuted(!isMuted); [cite: 11]
    };

    // JSX structure remains largely the same
    return (
        <main className="flex min-h-screen flex-col items-center justify-center bg-black p-4">
            <div className="w-full max-w-4xl mx-auto flex flex-col items-center space-y-8">
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-blue-500 mb-2">JARVIS</h1> [cite: 11]
                    <p className="text-gray-400">Just A Rather Very Intelligent System</p> [cite: 11]
                </div>

                <div className="relative w-full aspect-video bg-gray-900 rounded-xl overflow-hidden flex items-center justify-center"> [cite: 12]
                    <canvas ref={canvasRef} width={800} height={200} className="absolute inset-0 w-full h-full opacity-70" /> [cite: 12]

                    <div className="z-10 text-center p-8"> [cite: 12]
                        {isActive ? ( [cite: 12]
                            <div className="space-y-6"> [cite: 13]
                                {isLoading ? ( [cite: 13]
                                    <div className="flex justify-center"> [cite: 13]
                                        <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div> [cite: 13]
                                    </div>
                                ) : (
                                    <p className="text-blue-400 text-xl">{response}</p> [cite: 14]
                                )}
                            </div>
                        ) : (
                            <p className="text-gray-500 text-lg">Click the button below to activate Jarvis</p> [cite: 14]
                        )}
                    </div>
                </div>

                <div className="flex items-center justify-center space-x-6"> [cite: 15]
                    {!isActive ? ( [cite: 15]
                        <button
                            onClick={handleActivate} [cite: 16]
                            className="w-24 h-24 rounded-full bg-gradient-to-r from-blue-600 to-blue-400 flex items-center justify-center shadow-lg hover:shadow-blue-500/50 transition-all duration-300 hover:scale-105" [cite: 16]
                        >
                            <div className="w-20 h-20 rounded-full bg-blue-900 flex items-center justify-center"> [cite: 16]
                                <div className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-cyan-400 flex items-center justify-center pulse-animation"> [cite: 17]
                                    <span className="text-white font-bold">JARVIS</span> [cite: 17]
                                </div>
                            </div>
                        </button>
                    ) : (
                        <Button
                            onClick={handleStop} [cite: 18]
                            variant="destructive" // This prop might need adjustment based on your Button component
                            size="lg" // This prop might need adjustment
                            className="rounded-full w-16 h-16 flex items-center justify-center" [cite: 18]
                        >
                            <Square className="h-6 w-6" /> [cite: 18]
                        </Button>
                    )}

                    <Button
                        onClick={toggleMute} [cite: 19]
                        variant="outline" // Adjust as needed
                        size="icon" // Adjust as needed
                        className="rounded-full w-12 h-12 bg-gray-800 border-gray-700" [cite: 19]
                    >
                        {isMuted ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />} [cite: 20]
                    </Button>
                </div>
            </div>
        </main>
    );
}