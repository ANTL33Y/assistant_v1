// Dummy API simulating streaming chat responses
import { ChatMessage } from './types'

export async function sendMessage(
  messages: ChatMessage[]
): Promise<ChatMessage> {
  const content = 'Elysia here! This is a canned response.'
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ id: Date.now().toString(), role: 'assistant', content })
    }, 1000)
  })
}
