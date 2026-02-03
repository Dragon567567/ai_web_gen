import { useState } from 'react';
import ChatPanel from '@/components/ChatPanel';
import PreviewPanel from '@/components/PreviewPanel';
import CodeEditor from '@/components/CodeEditor';
import { Message, GeneratedCode } from '@/types';
import { aiService } from '@/services/AIService';

export default function Index() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [generatedCode, setGeneratedCode] = useState<GeneratedCode | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [showCodeEditor, setShowCodeEditor] = useState(false);

  const handleSendMessage = async (content: string) => {
    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content,
      timestamp: Date.now()
    };
    setMessages(prev => [...prev, userMessage]);

    // 开始生成
    setIsGenerating(true);

    try {
      // 流式显示AI响应
      const streamMessages: string[] = [];
      for await (const chunk of aiService.streamResponse(content)) {
        streamMessages.push(chunk);
        const assistantMessage: Message = {
          id: `${Date.now()}-assistant`,
          role: 'assistant',
          content: streamMessages.join('\n'),
          timestamp: Date.now()
        };
        
        setMessages(prev => {
          const filtered = prev.filter(m => m.id !== `${Date.now()}-assistant`);
          return [...filtered, assistantMessage];
        });
      }

      // 生成代码
      const code = await aiService.generateCode(content);
      setGeneratedCode(code);

      // 添加完成消息
      const finalMessage: Message = {
        id: `${Date.now()}-final`,
        role: 'assistant',
        content: '✅ 代码生成完成！您可以在右侧预览效果，或点击"查看代码"按钮查看源代码。',
        timestamp: Date.now()
      };
      
      setMessages(prev => {
        const filtered = prev.filter(m => !m.id.includes('assistant'));
        return [...filtered, finalMessage];
      });

    } catch (error) {
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: '抱歉，生成代码时出现错误。请重试。',
        timestamp: Date.now()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="h-screen flex bg-[#0A0A0A]">
      {/* Left Panel - Chat */}
      <div className="w-[40%] h-full">
        <ChatPanel
          messages={messages}
          onSendMessage={handleSendMessage}
          isGenerating={isGenerating}
        />
      </div>

      {/* Right Panel - Preview */}
      <div className="flex-1 h-full">
        <PreviewPanel
          code={generatedCode}
          onShowCode={() => setShowCodeEditor(true)}
        />
      </div>

      {/* Code Editor Modal */}
      {showCodeEditor && generatedCode && (
        <CodeEditor
          code={generatedCode}
          onClose={() => setShowCodeEditor(false)}
        />
      )}
    </div>
  );
}