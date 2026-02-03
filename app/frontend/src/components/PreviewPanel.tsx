import { useEffect, useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { RefreshCw, Maximize2, Code2 } from 'lucide-react';
import { GeneratedCode } from '@/types';

interface PreviewPanelProps {
  code: GeneratedCode | null;
  onShowCode: () => void;
}

export default function PreviewPanel({ code, onShowCode }: PreviewPanelProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  useEffect(() => {
    if (code && iframeRef.current) {
      updatePreview();
    }
  }, [code]);

  const updatePreview = () => {
    if (!code || !iframeRef.current) return;

    const iframe = iframeRef.current;
    const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;

    if (iframeDoc) {
      const fullHTML = `
        <!DOCTYPE html>
        <html lang="zh-CN">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style>${code.css}</style>
        </head>
        <body>
          ${code.html.replace(/<link[^>]*>/g, '').replace(/<script[^>]*src[^>]*><\/script>/g, '')}
          <script>${code.javascript}</script>
        </body>
        </html>
      `;

      iframeDoc.open();
      iframeDoc.write(fullHTML);
      iframeDoc.close();
    }
  };

  const handleRefresh = () => {
    setIsRefreshing(true);
    updatePreview();
    setTimeout(() => setIsRefreshing(false), 500);
  };

  const handleFullscreen = () => {
    if (iframeRef.current) {
      iframeRef.current.requestFullscreen();
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#0A0A0A]">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-[#2A2A2A]">
        <div className="flex items-center gap-3">
          <img 
            src="https://mgx-backend-cdn.metadl.com/generate/images/947756/2026-02-03/7ae694b7-0026-4c24-a5b1-f819287f07ab.png" 
            alt="Preview" 
            className="w-6 h-6"
          />
          <h2 className="text-lg font-semibold text-white">实时预览</h2>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={onShowCode}
            className="bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
          >
            <Code2 className="w-4 h-4 mr-2" />
            查看代码
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
          </Button>
          <Button
            variant="outline"
            size="sm"
            onClick={handleFullscreen}
            className="bg-[#1A1A1A] border-[#2A2A2A] text-[#9CA3AF] hover:bg-[#2A2A2A] hover:text-white"
          >
            <Maximize2 className="w-4 h-4" />
          </Button>
        </div>
      </div>

      {/* Preview */}
      <div className="flex-1 relative bg-white">
        {!code ? (
          <div className="absolute inset-0 flex items-center justify-center bg-[#0A0A0A]">
            <div className="text-center">
              <div className="w-24 h-24 mx-auto mb-4 rounded-full bg-[#1A1A1A] flex items-center justify-center">
                <img 
                  src="https://mgx-backend-cdn.metadl.com/generate/images/947756/2026-02-03/a1e8ad55-b48b-4171-bc62-1e420e88a3fc.png" 
                  alt="Code" 
                  className="w-12 h-12"
                />
              </div>
              <p className="text-[#9CA3AF] text-lg">等待AI生成代码...</p>
              <p className="text-[#6B7280] text-sm mt-2">在左侧输入你的需求开始</p>
            </div>
          </div>
        ) : (
          <iframe
            ref={iframeRef}
            className="w-full h-full border-0"
            title="预览"
            sandbox="allow-scripts allow-same-origin"
          />
        )}
      </div>
    </div>
  );
}