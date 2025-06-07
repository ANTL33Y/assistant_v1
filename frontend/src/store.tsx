// Minimal global state management using Context and Reducer
import { createContext, useContext, useReducer, ReactNode } from 'react'
import { ChatMessage } from './types'

type State = {
  messages: ChatMessage[]
  streaming: boolean
  sidebarOpen: boolean
}

type Action =
  | { type: 'addMessage'; message: ChatMessage }
  | { type: 'setStreaming'; value: boolean }
  | { type: 'toggleSidebar' }
  | { type: 'resetMessages' }

const initialState: State = {
  messages: [],
  streaming: false,
  sidebarOpen: false
}

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'addMessage':
      return { ...state, messages: [...state.messages, action.message] }
    case 'setStreaming':
      return { ...state, streaming: action.value }
    case 'toggleSidebar':
      return { ...state, sidebarOpen: !state.sidebarOpen }
    case 'resetMessages':
      return { ...state, messages: [] }
    default:
      return state
  }
}

const StoreContext = createContext<[State, React.Dispatch<Action>]>([
  initialState,
  () => {}
])

export function StoreProvider({ children }: { children: ReactNode }) {
  const value = useReducer(reducer, initialState)
  return <StoreContext.Provider value={value}>{children}</StoreContext.Provider>
}

export function useStore() {
  return useContext(StoreContext)
}
