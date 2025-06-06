const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'
import type { ChatMessage } from './types'

export async function sendMessage(messages: ChatMessage[]): Promise<ChatMessage> {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ messages })
  })
  if (!res.ok) {
    throw new Error('Failed to send message')
  }
  const data = await res.json()
  return {
    id: Date.now().toString(),
    role: 'assistant',
    content: data.text || ''
  }
}

export async function speechToText(blob: Blob): Promise<string> {
  const form = new FormData()
  form.append('file', blob, 'audio.wav')
  const res = await fetch(`${BASE_URL}/speech-to-text`, {
    method: 'POST',
    body: form
  })
  if (!res.ok) {
    throw new Error('Failed to transcribe audio')
  }
  const data = await res.json()
  return data.text || ''
}

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${BASE_URL}/health`)
    return res.ok
  } catch {
    return false
  }
}
