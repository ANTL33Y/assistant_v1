import { useState } from 'react'
import { Sidebar } from './components/Sidebar'
import { ChatMessage } from './components/ChatMessage'
import { Composer } from './components/Composer'

export default function App() {
  const [messages, setMessages] = useState([
    { author: 'User', content: 'Hello' },
    { author: 'AI', content: 'Hi there!' },
  ])

  const handleSend = (text: string) => {
    setMessages((m) => [...m, { author: 'User', content: text }])
  }

  return (
    <div className="flex h-screen text-[#E8EAEE]">
      <Sidebar items={["First chat", "Second chat"]} />
      <Sidebar mobile items={["First chat", "Second chat"]} />
      <main className="flex-1 flex flex-col bg-chat-gradient p-6 overflow-y-auto space-y-6">
        <div className="flex-1 space-y-6">
          {messages.map((m, i) => (
            <ChatMessage key={i} author={m.author} content={m.content} />
          ))}
        </div>
      </main>
      <Composer onSend={handleSend} />
    </div>
  )
}
