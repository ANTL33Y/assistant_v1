import { useState } from 'react'

export function useSpeechSynthesis() {
  const [speaking, setSpeaking] = useState(false)

  const speak = (text: string) => {
    const synth = window.speechSynthesis
    if (!synth) return
    const utter = new SpeechSynthesisUtterance(text)
    utter.onstart = () => setSpeaking(true)
    utter.onend = () => setSpeaking(false)
    synth.speak(utter)
  }

  return { speak, speaking }
}
