import { motion } from 'framer-motion'
import ReactMarkdown from 'react-markdown'
import rehypeHighlight from 'rehype-highlight'
import { ThumbsUp, MoreHorizontal } from 'lucide-react'

interface ChatMessageProps {
  author: string
  content: string
}

export function ChatMessage({ author, content }: ChatMessageProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.2 }}
      className="space-y-2"
    >
      <div className="text-sm font-bold text-muted">{author}</div>
      <div className="prose prose-invert max-w-none text-base leading-relaxed">
        <ReactMarkdown
          rehypePlugins={[rehypeHighlight]}
          components={{
            code({ className, children, ...rest }) {
              const inline = !(className && className.includes('language-'))
              if (inline) {
                return (
                  <code className="bg-code-bg/50 px-1 rounded" {...rest}>
                    {children}
                  </code>
                )
              }
              return (
                <pre className="bg-code-bg p-4 rounded-md text-sm font-mono overflow-auto">
                  <code className={className} {...rest}>
                    {children}
                  </code>
                </pre>
              )
            },
            img(props) {
              return (
                <img
                  className="w-[200px] rounded-lg border border-white/10"
                  {...props}
                />
              )
            }
          }}
        >
          {content}
        </ReactMarkdown>
      </div>
      <div className="flex space-x-3 text-muted text-sm">
        <ThumbsUp size={16} className="cursor-pointer hover:opacity-80" />
        <MoreHorizontal size={16} className="cursor-pointer hover:opacity-80" />
      </div>
    </motion.div>
  )
}
