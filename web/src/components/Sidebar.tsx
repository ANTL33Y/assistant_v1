import { Disclosure } from '@headlessui/react'
import { motion } from 'framer-motion'

interface SidebarProps {
  items: string[]
  mobile?: boolean
}

export function Sidebar({ items, mobile }: SidebarProps) {
  const content = (
    <div className="h-full flex flex-col text-sm p-4 space-y-4 bg-sidebar">
      <div className="flex items-center justify-between">
        <span className="tracking-wider text-lg font-semibold">ELYSIA</span>
        <div className="flex space-x-2">
          <div className="w-6 h-6 bg-gray-600 rounded-full" />
          <div className="w-6 h-6 bg-gray-600 rounded-full" />
        </div>
      </div>
      <input type="text" placeholder="Search" className="rounded-md bg-[#1A1F27] px-2 py-1 text-sm" />
      <div className="text-muted uppercase text-xs">Recent</div>
      <div className="flex-1 overflow-y-auto space-y-1">
        {items.map((t) => (
          <div key={t} className="p-2 rounded hover:bg-white/5 cursor-pointer" >{t}</div>
        ))}
      </div>
    </div>
  )

  if (mobile) {
    return (
      <Disclosure as="div" className="lg:hidden">
        {({ open }) => (
          <>
            <Disclosure.Button className="p-2">☰</Disclosure.Button>
            <Disclosure.Panel>
              <motion.div initial={{ x: -280 }} animate={{ x: open ? 0 : -280 }} className="fixed inset-y-0 left-0 w-64 z-20">
                {content}
              </motion.div>
            </Disclosure.Panel>
          </>
        )}
      </Disclosure>
    )
  }

  return <aside className="w-[280px] border-r border-white/10 hidden lg:block">{content}</aside>
}
