import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Send, Loader2 } from 'lucide-react';
import { Message } from '@/types';

interface ChatPanelProps {
  messages: Message[];
  onSendMessage: (content: string) => void;
  isGenerating: boolean;
}

export default function ChatPanel({ messages, onSendMessage, isGenerating }: ChatPanelProps) {
  const [input, setInput] = useState('');
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    if (input.trim() && !isGenerating) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#0A0A0A] border-r border-[#2A2A2A]">
      {/* Header */}
      <div className="p-6 border-b border-[#2A2A2A]">
        <div className="flex items-center gap-3">
          <img 
            src="https://mgx-backend-cdn.metadl.com/generate/images/947756/2026-02-03/156803cf-57c8-4490-bd72-b524372384f1.png" 
            alt="Chat" 
            className="w-8 h-8"
          />
          <div>
            <h2 className="text-xl font-bold text-white">AI代码助手</h2>
            <p className="text-sm text-[#9CA3AF]">描述你想要的应用</p>
          </div>
        </div>
      </div>

      {/* Messages */}
      <ScrollArea className="flex-1 p-6" ref={scrollRef}>
        <div className="space-y-4">
          {messages.length === 0 && (
            <div className="text-center py-12">
              <img 
                src="https://mgx-backend-cdn.metadl.com/generate/images/947756/2026-02-03/fd29a045-7a51-4fd6-819d-35cfe69b3241.png" 
                alt="AI Coding" 
                className="w-full max-w-md mx-auto rounded-lg mb-6 opacity-80"
              />
              <p className="text-[#9CA3AF] text-lg">开始对话，让AI为你生成代码</p>
              <div className="mt-6 space-y-2">
                <p className="text-sm text-[#6B7280]">试试这些示例：</p>
                <div className="flex flex-wrap gap-2 justify-center">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInput('创建一个计数器应用')}
                    className="bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
                  >
                    计数器应用
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInput('创建一个待办事项列表')}
                    className="bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
                  >
                    待办列表
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setInput('创建一个简单的个人主页')}
                    className="bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
                  >
                    个人主页
                  </Button>
                </div>
              </div>
            </div>
          )}
          
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-lg p-4 ${
                  message.role === 'user'
                    ? 'bg-[#6366F1] text-white'
                    : 'bg-[#1A1A1A] text-[#E5E7EB] border border-[#2A2A2A]'
                }`}
              >
                <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
                <p className="text-xs mt-2 opacity-60">
                  {new Date(message.timestamp).toLocaleTimeString('zh-CN', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
            </div>
          ))}

          {isGenerating && (
            <div className="flex justify-start">
              <div className="bg-[#1A1A1A] text-[#E5E7EB] border border-[#2A2A2A] rounded-lg p-4">
                <div className="flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span className="text-sm">AI正在生成代码...</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </ScrollArea>

      {/* Input */}
      <div className="p-6 border-t border-[#2A2A2A]">
        <div className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="描述你想要创建的应用..."
            className="flex-1 min-h-[60px] max-h-[120px] bg-[#1A1A1A] border-[#2A2A2A] text-white placeholder:text-[#6B7280] focus:border-[#6366F1] resize-none"
            disabled={isGenerating}
          />
          <Button
            onClick={handleSend}
            disabled={!input.trim() || isGenerating}
            className="bg-[#6366F1] hover:bg-[#5558E3] text-white px-6"
          >
            {isGenerating ? (
              <Loader2 className="w-5 h-5 animate-spin" />
            ) : (
              <Send className="w-5 h-5" />
            )}
          </Button>
        </div>
      </div>
    </div>
  );
}