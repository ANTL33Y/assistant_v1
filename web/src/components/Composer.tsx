import { Send } from 'lucide-react'
import { useState } from 'react'

interface ComposerProps {
  onSend?: (text: string) => void
}

export function Composer({ onSend }: ComposerProps) {
  const [text, setText] = useState('')

  const handleSend = () => {
    if (!text.trim()) return
    onSend?.(text)
    setText('')
  }

  return (
    <div className="fixed bottom-6 left-[calc(280px+24px)] right-6 lg:left-[calc(280px+24px)]">
      <div className="flex items-center bg-code-bg border border-[#1A1F27] rounded-full px-4 py-2">
        <button className="mr-2">➕</button>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="flex-1 bg-transparent resize-none focus:outline-none h-6 max-h-40 overflow-y-auto"
          rows={1}
        />
        <button onClick={handleSend} className="ml-2">
          <Send size={20} />
        </button>
      </div>
    </div>
  )
}
