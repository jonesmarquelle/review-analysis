import type { Metadata } from 'next'
 
export const metadata: Metadata = {
  title: 'Review Analysis',
  description: 'Review Analysis is a tool that analyzes reviews and provides insights into the business.',
}

export default function RootLayout({
    children,
  }: {
    children: React.ReactNode
  }) {
    return (
    <html lang="en">
        <body>
            <div id="root">{children}</div>
        </body>
    </html>
    )
  }