// Bottom input bar with textarea and voice button
import { FormEvent, useEffect, useRef, useState } from 'react'
import { PaperAirplaneIcon } from '@heroicons/react/24/outline'
import { useStore } from '../store'
import { sendMessage } from '../api'
import { ChatMessage } from '../types'
import VoiceButton from './VoiceButton'

interface Props {
  onVoiceInput: (text: string) => void
inputRef?: React.RefObject<HTMLTextAreaElement>
}

export default function PromptBar({ onVoiceInput, inputRef }: Props) {
  const [state, dispatch] = useStore()
  const [value, setValue] = useState('')
  const [rows, setRows] = useState(1)
  const ref = inputRef ?? useRef<HTMLTextAreaElement>(null)

  const send = async (text: string) => {
    if (!text.trim()) return
    const userMsg: ChatMessage = { id: Date.now().toString(), role: 'user', content: text }
    dispatch({ type: 'addMessage', message: userMsg })
    setValue('')
    dispatch({ type: 'setStreaming', value: true })
    const assistantMsg = await sendMessage([...state.messages, userMsg])
    dispatch({ type: 'addMessage', message: assistantMsg })
    dispatch({ type: 'setStreaming', value: false })
  }

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    send(value)
  }

  useEffect(() => {
    const textarea = ref.current
    if (!textarea) return
    textarea.style.height = 'auto'
    textarea.style.height = textarea.scrollHeight + 'px'
    const newRows = Math.min(6, Math.floor(textarea.scrollHeight / 24))
    setRows(newRows)
  }, [value])

  useEffect(() => {
    if (onVoiceInput) {
      onVoiceInput('')
    }
  }, [onVoiceInput])

  return (
    <form onSubmit={handleSubmit} className="border-t border-gray-300/40 dark:border-black/20 p-4 flex items-end gap-2">
      <textarea
        ref={ref}
        rows={rows}
        value={value}
        onChange={e => setValue(e.target.value)}
        placeholder="Send a message"
        className="flex-1 resize-none bg-transparent focus:outline-none"
        onKeyDown={e => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            send(value)
          }
        }}
      />
      <VoiceButton onTranscript={text => send(text)} />
      <button
        type="submit"
        className="p-2 disabled:opacity-50"
        aria-label="Send"
      >
        <PaperAirplaneIcon className="h-5 w-5 rotate-90" />
      </button>
    </form>
  )
}
