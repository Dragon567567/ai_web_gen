import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Copy, Check, Download } from 'lucide-react';
import { GeneratedCode } from '@/types';

interface CodeEditorProps {
  code: GeneratedCode;
  onClose: () => void;
}

export default function CodeEditor({ code, onClose }: CodeEditorProps) {
  const [copiedTab, setCopiedTab] = useState<string | null>(null);

  const copyToClipboard = (text: string, tab: string) => {
    navigator.clipboard.writeText(text);
    setCopiedTab(tab);
    setTimeout(() => setCopiedTab(null), 2000);
  };

  const downloadCode = () => {
    const zip = `
HTML文件:
${code.html}

---

CSS文件:
${code.css}

---

JavaScript文件:
${code.javascript}
    `;

    const blob = new Blob([zip], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generated-code.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-[#0A0A0A] border border-[#2A2A2A] rounded-lg w-full max-w-4xl h-[80vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-[#2A2A2A]">
          <h2 className="text-xl font-bold text-white">生成的代码</h2>
          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={downloadCode}
              className="bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
            >
              <Download className="w-4 h-4 mr-2" />
              下载
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={onClose}
              className="bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
            >
              关闭
            </Button>
          </div>
        </div>

        {/* Code Tabs */}
        <Tabs defaultValue="html" className="flex-1 flex flex-col">
          <TabsList className="bg-[#1A1A1A] border-b border-[#2A2A2A] rounded-none p-2">
            <TabsTrigger 
              value="html"
              className="data-[state=active]:bg-[#6366F1] data-[state=active]:text-white"
            >
              HTML
            </TabsTrigger>
            <TabsTrigger 
              value="css"
              className="data-[state=active]:bg-[#6366F1] data-[state=active]:text-white"
            >
              CSS
            </TabsTrigger>
            <TabsTrigger 
              value="javascript"
              className="data-[state=active]:bg-[#6366F1] data-[state=active]:text-white"
            >
              JavaScript
            </TabsTrigger>
          </TabsList>

          <TabsContent value="html" className="flex-1 m-0 relative">
            <Button
              variant="outline"
              size="sm"
              onClick={() => copyToClipboard(code.html, 'html')}
              className="absolute top-4 right-4 z-10 bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
            >
              {copiedTab === 'html' ? (
                <>
                  <Check className="w-4 h-4 mr-2" />
                  已复制
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 mr-2" />
                  复制
                </>
              )}
            </Button>
            <ScrollArea className="h-full">
              <pre className="p-6 text-sm font-mono text-[#E5E7EB] bg-[#0A0A0A]">
                <code>{code.html}</code>
              </pre>
            </ScrollArea>
          </TabsContent>

          <TabsContent value="css" className="flex-1 m-0 relative">
            <Button
              variant="outline"
              size="sm"
              onClick={() => copyToClipboard(code.css, 'css')}
              className="absolute top-4 right-4 z-10 bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
            >
              {copiedTab === 'css' ? (
                <>
                  <Check className="w-4 h-4 mr-2" />
                  已复制
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 mr-2" />
                  复制
                </>
              )}
            </Button>
            <ScrollArea className="h-full">
              <pre className="p-6 text-sm font-mono text-[#E5E7EB] bg-[#0A0A0A]">
                <code>{code.css}</code>
              </pre>
            </ScrollArea>
          </TabsContent>

          <TabsContent value="javascript" className="flex-1 m-0 relative">
            <Button
              variant="outline"
              size="sm"
              onClick={() => copyToClipboard(code.javascript, 'javascript')}
              className="absolute top-4 right-4 z-10 bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
            >
              {copiedTab === 'javascript' ? (
                <>
                  <Check className="w-4 h-4 mr-2" />
                  已复制
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 mr-2" />
                  复制
                </>
              )}
            </Button>
            <ScrollArea className="h-full">
              <pre className="p-6 text-sm font-mono text-[#E5E7EB] bg-[#0A0A0A]">
                <code>{code.javascript}</code>
              </pre>
            </ScrollArea>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}