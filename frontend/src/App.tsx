// Top-level layout replicating ChatGPT's interface
import { useEffect, useState, useRef } from 'react'
import { StoreProvider, useStore } from './store'
import MessageList from './components/MessageList'
import PromptBar from './components/PromptBar'
import { MoonIcon, SunIcon, PlusIcon } from '@heroicons/react/24/outline'
import { useSpeechSynthesis } from './hooks/useSpeechSynthesis'

function Sidebar() {
  const [state, dispatch] = useStore()
  const [dark, setDark] = useState(
    localStorage.getItem('theme') !== 'light'
  )

  useEffect(() => {
    document.documentElement.classList.toggle('dark', dark)
    localStorage.setItem('theme', dark ? 'dark' : 'light')
  }, [dark])

  return (
    <aside
      className={`${
        state.sidebarOpen ? 'block' : 'hidden'
      } md:block w-64 shrink-0 bg-gray-200/50 dark:bg-[#202123] border-r border-gray-300/40 dark:border-black/20`}
    >
      <div className="p-4 flex items-center justify-between">
        <button
          onClick={() => dispatch({ type: 'toggleSidebar' })}
          className="md:hidden p-2"
        >
          ✕
        </button>
        <button
          onClick={() => dispatch({ type: 'resetMessages' })}
          className="p-2 flex items-center gap-1"
        >
          <PlusIcon className="h-4 w-4" /> New Chat
        </button>
        <button onClick={() => setDark(!dark)} className="p-2">
          {dark ? <SunIcon className="h-5 w-5" /> : <MoonIcon className="h-5 w-5" />}
        </button>
      </div>
      <ul className="p-2 space-y-1 text-sm">
        <li className="px-2 py-1 rounded bg-gray-300/50 dark:bg-black/20">Conversation 1</li>
      </ul>
    </aside>
  )
}

function ChatPanel() {
  const [state, dispatch] = useStore()
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const { speak } = useSpeechSynthesis()

  useEffect(() => {
    const handleShortcut = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === '/') {
        e.preventDefault()
        dispatch({ type: 'toggleSidebar' })
      }
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        inputRef.current?.focus()
      }
    }
    window.addEventListener('keydown', handleShortcut)
    return () => window.removeEventListener('keydown', handleShortcut)
  }, [dispatch])

  useEffect(() => {
    const last = state.messages[state.messages.length - 1]
    if (last && last.role === 'assistant') {
      speak(last.content)
    }
  }, [state.messages, speak])

  return (
    <div className="flex flex-col flex-1 h-screen bg-gradient-to-b from-white via-gray-50 to-gray-100 dark:from-[#2b2d30] dark:via-[#202123] dark:to-[#111]">
      <div className="flex-1 flex flex-col">
        <MessageList messages={state.messages} />
      </div>
      <PromptBar inputRef={inputRef} onVoiceInput={() => {}} />
    </div>
  )
}

export default function App() {
  return (
    <StoreProvider>
      <div className="flex h-screen">
        <Sidebar />
        <ChatPanel />
      </div>
    </StoreProvider>
  )
}
