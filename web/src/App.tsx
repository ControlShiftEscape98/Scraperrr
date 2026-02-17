
import { useState, useEffect } from 'react'
import { supabase } from './lib/supabase'
import { FlowGradient } from './components/FlowGradient'
import { FocusRail, type FocusRailItem } from './components/ui/focus-rail'

// Placeholder images for articles since we don't scrape OG images yet
const STOCK_IMAGES = [
    "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=1000&auto=format&fit=crop", // AI/Neural
    "https://images.unsplash.com/photo-1677442136019-21780ecad995?q=80&w=1000&auto=format&fit=crop", // Robot hand
    "https://images.unsplash.com/photo-1555255707-c07966088b7b?q=80&w=1000&auto=format&fit=crop", // Code
    "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1000&auto=format&fit=crop", // Chip
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=1000&auto=format&fit=crop", // Cyber
    "https://images.unsplash.com/photo-1593508512255-86ab42a8e620?q=80&w=1000&auto=format&fit=crop", // VR
]

type Article = {
    id: string
    title: string
    url: string
    source: string
    scraped_at: string
}

function App() {
    const [articles, setArticles] = useState<FocusRailItem[]>([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchArticles()
    }, [])

    async function fetchArticles() {
        try {
            const { data, error } = await supabase
                .from('articles')
                .select('*')
                .order('scraped_at', { ascending: false })
                .limit(20)

            if (error) throw error

            const mappedItems: FocusRailItem[] = (data || []).map((article: Article, index: number) => ({
                id: article.id,
                title: article.title,
                description: `${article.source} • ${new Date(article.scraped_at).toLocaleDateString()}`,
                meta: article.source,
                imageSrc: STOCK_IMAGES[index % STOCK_IMAGES.length],
                href: article.url
            }))

            setArticles(mappedItems)
        } catch (error) {
            console.error('Error fetching articles:', error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="relative min-h-screen w-full overflow-hidden text-white">
            {/* Background Gradient */}
            <FlowGradient />

            <div className="relative z-10 flex flex-col items-center justify-center py-20 min-h-screen">
                {/* Header */}
                <div className="mb-12 text-center">
                    <h1 className="text-6xl md:text-8xl font-heading font-bold text-primary mb-2 tracking-tighter">
                        SCRAPER<span className="text-accent">RR</span>
                    </h1>
                    <p className="text-accent text-sm md:text-base uppercase tracking-[0.2em]">
                        Daily Intelligence Feed
                    </p>
                </div>

                {/* Content Rail */}
                {loading ? (
                    <div className="text-accent animate-pulse">Initializing Feed...</div>
                ) : (
                    <div className="w-full">
                        {articles.length > 0 ? (
                            <FocusRail
                                items={articles}
                                autoPlay={false}
                                loop={true}
                            />
                        ) : (
                            <div className="text-center text-accent">No articles found. Run the scraper!</div>
                        )}
                    </div>
                )}

                {/* Footer */}
                <footer className="mt-12 text-accent text-xs">
                    &copy; {new Date().getFullYear()} Scraperrr Systems.
                </footer>
            </div>
        </div>
    )
}

export default App
