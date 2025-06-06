// Button that toggles speech recognition
import { useEffect } from 'react'
import { MicrophoneIcon } from '@heroicons/react/24/solid'
import { useSpeechRecognition } from '../hooks/useSpeechRecognition'

interface Props {
  onTranscript: (text: string) => void
}

export default function VoiceButton({ onTranscript }: Props) {
  const { isListening, transcript, start, stop, error } = useSpeechRecognition()

  useEffect(() => {
    if (!isListening && transcript) {
      onTranscript(transcript)
    }
  }, [isListening, transcript, onTranscript])

  if (error) {
    return (
      <button type="button" className="p-2" title={error} disabled>
        <MicrophoneIcon className="h-5 w-5" />
      </button>
    )
  }

  return (
    <button
      type="button"
      onClick={isListening ? stop : start}
      className={
        isListening ? 'animate-pulse text-red-500 p-2' : 'p-2 text-gray-500'
      }
      aria-label="Voice input"
    >
      <MicrophoneIcon className="h-5 w-5" />
    </button>
  )
}
