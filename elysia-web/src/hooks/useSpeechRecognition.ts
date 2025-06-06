// Hook wrapping the Web Speech API for voice input
import { useEffect, useRef, useState } from 'react'

export function useSpeechRecognition() {
  const [isListening, setListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const [error, setError] = useState<string | null>(null)
  const recognitionRef = useRef<SpeechRecognition | null>(null)

  useEffect(() => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
    if (!SpeechRecognition) {
      setError('Speech recognition not supported')
      return
    }
    recognitionRef.current = new SpeechRecognition()
    recognitionRef.current.continuous = true
    recognitionRef.current.interimResults = true
    recognitionRef.current.lang = 'en-US'

    const handleResult = (e: SpeechRecognitionEvent) => {
      let final = ''
      let interim = ''
      for (const res of e.results) {
        const text = res[0].transcript
        if (res.isFinal) final += text
        else interim += text
      }
      setTranscript(final || interim)
    }

    const handleEnd = () => {
      setListening(false)
    }

    recognitionRef.current.addEventListener('result', handleResult)
    recognitionRef.current.addEventListener('end', handleEnd)

    return () => {
      recognitionRef.current?.removeEventListener('result', handleResult)
      recognitionRef.current?.removeEventListener('end', handleEnd)
      recognitionRef.current?.stop()
    }
  }, [])

  const start = () => {
    if (recognitionRef.current && !isListening) {
      setTranscript('')
      setListening(true)
      recognitionRef.current.start()
    }
  }

  const stop = () => {
    recognitionRef.current?.stop()
  }

  return { isListening, transcript, start, stop, error }
}
