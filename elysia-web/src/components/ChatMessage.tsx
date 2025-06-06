// Individual chat bubble for user or assistant messages
import { ChatMessage as Msg } from '../types'
import { clsx } from 'clsx'

interface Props {
  message: Msg
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === 'user'
  const base = 'rounded-lg px-4 py-2 whitespace-pre-wrap prose dark:prose-invert'
  const userStyles =
    'bg-white dark:bg-[#343541] border border-gray-300/60 dark:border-[#3e3f4b] self-end'
  const assistantStyles = 'bg-[#f7f7f8] dark:bg-[#444654]'
  return (
    <div className={clsx('my-2 flex', isUser ? 'justify-end' : 'justify-start')}>
      <div className={clsx(base, isUser ? userStyles : assistantStyles)}>
        {message.content}
      </div>
    </div>
  )
}
