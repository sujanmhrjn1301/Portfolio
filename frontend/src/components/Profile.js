import React, { useState, useEffect } from 'react';
import { ExternalLink, X, UserCircle, Book, TrendingUp, GitBranch, Target, Medal, Heart, MessageCircle, Instagram, Github, Linkedin, Phone, Mail } from 'lucide-react';
import whatsappIcon from '../imgs/whatsapp.svg';
import viberIcon from '../imgs/viber.svg';

function Profile({ portfolioInfo, projects, onClose }) {
  const [activeTab, setActiveTab] = useState('personal');
  
  // ESC key listener to close modal
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);
  
  // Icon mapping for tabs
  const iconMap = {
    personal: UserCircle,
    academic: Book,
    experience: TrendingUp,
    projects: GitBranch,
    skills: Target,
    certifications: Medal,
    hobbies: Heart,
    socials: MessageCircle
  };
  
  // Settings Modal Tabs
  const tabs = [
    { id: 'personal', label: 'Personal Info' },
    { id: 'academic', label: 'Academic Info' },
    { id: 'experience', label: 'Industry Experience' },
    { id: 'projects', label: 'Projects' },
    { id: 'skills', label: 'Skills' },
    { id: 'certifications', label: 'Certifications' },
    { id: 'hobbies', label: 'Hobbies' },
    { id: 'socials', label: 'Social Media' },
  ];

  const cvData = {
    name: "Sujan Maharjan",
    location: "Thecho, Lalitpur, Nepal",
    email: "mhrjnsujan.official@gmail.com",
    phone: "+977-9860942721",
    bio: "A self-motivated and adaptable individual with a strong aptitude for rapid learning, a keen openness to innovative concepts, and a growth mindset. Open-minded to feedback as a valuable opportunity for growth and continuous improvement.",
    
    experience: [
      {
        title: "Security Research Analyst",
        company: "SecurityPal",
        location: "Baluwatar, Kathmandu",
        period: "Dec, 2024 - January, 2025",
        highlights: [
          "Led the New Analyst apprenticeship program, mentoring and onboarding fresh talent.",
          "Drove process innovations and improvements, streamlining workflows to enhance efficiency, accuracy, and overall team productivity.",
          "Collaborated with multiple cross-functional teams on key projects, ensuring effective knowledge-sharing and timely project execution.",
          "Strengthened client trust by delivering high-quality data, actionable insights, and reliable recommendations."
        ]
      },
      {
        title: "New Analyst",
        company: "SecurityPal",
        location: "Baluwatar, Kathmandu",
        period: "Jun, 2024 - Sep, 2024",
        highlights: [
          "Gained knowledge in the GRC sector and various regulatory compliance frameworks while conducting security assessments and data analysis."
        ]
      }
    ],

    education: [
      {
        level: "Bachelor's in Information Technology",
        school: "Presidential Graduate School",
        location: "Kathmandu",
        period: "Apr, 2022 - Present"
      },
      {
        level: "+2",
        school: "Shree Bajrabarahi Secondary School",
        location: "Lalitpur",
        period: "Oct, 2018 - Mar, 2021",
        gpa: "3.37 GPA"
      },
      {
        level: "Secondary Education Examination",
        school: "Indreni Secondary English School",
        location: "Lalitpur",
        period: "Jul, 2018",
        gpa: "3.65 GPA"
      }
    ],

    projects: [
      {
        title: "Profanity Filter Discord Bot",
        description: "A profanity detection bot for discord server which detects profanity words and gives a warning and deletes the message. It is created to keep the discord chat servers clean.",
        link: "https://github.com/sujanmhrjn1301/Profanity-Detection-Bot.git"
      },
      {
        title: "Hakucha Discord Chatbot",
        description: "A friendly discord chatbot that replies to user's query as well as replies humorously to keep the chat server lively. Hakucha 2.0 is in development, with key features including web surfing capabilities and expanded input options such as images and videos.",
        link: "https://github.com/sujanmhrjn1301/Hakucha_Bot.git"
      },
      {
        title: "Hakucha (ChatGPT Clone)",
        description: "ChatGPT Clone using the OpenAI API and JS.",
        link: "https://github.com/sujanmhrjn1301/chatgpt-clone-hakucha.git"
      },
      {
        title: "Ki:Paa: Image Generator",
        description: "An AI Image Generator that generates image based on the prompt.",
        link: "https://github.com/sujanmhrjn1301/Ki-Paa--Image-Generator.git"
      },
      {
        title: "2FA",
        description: "Created a 2nd Factor Authentication using Twilio.",
        link: "https://github.com/sujanmhrjn1301/2FA.git"
      },
      {
        title: "Haku Voice Assistant",
        description: "A voice assistant application.",
        link: "https://github.com/sujanmhrjn1301/voice-assistant-haku.git"
      },
      {
        title: "UniBot",
        description: "A web-based chatbot that replies to user's queries regarding a college.",
        link: "https://github.com/sujanmhrjn1301/Uni-bot.git"
      },
      {
        title: "Netflix Clone",
        description: "A Netflix clone using HTML, CSS, NodeJS, MySQL (for Login).",
        link: "https://github.com/sujanmhrjn1301/netix-login-clone.git"
      },
      {
        title: "Sugoi-ani",
        description: "Developing an anime streaming website with a focus on user-friendly interface and seamless content delivery.",
        link: "https://github.com/sujanmhrjn1301/Sugoi-ani.git"
      }
    ],

    certifications: [
      { title: "Certified in Cybersecurity", issuer: "ISC2", year: "2025" },
      { title: "Analyzing Data Using Python: Data Analytics Using Pandas", issuer: "Skillsoft", year: "2024" },
      { title: "Cloud Foundations", issuer: "AWS", year: "2024" },
      { title: "Python for Data Science", issuer: "Great Learning", year: "2023" },
      { title: "Python Basics", issuer: "HackerRank", year: "2023" }
    ],

    hobbies: [
      { name: "Photography", description: "Passionate about capturing street photos, nature scenes, and occasional portraits. Every frame tells a story.", link: "https://www.instagram.com/mhrjn_sujan/" },
      { name: "Pencil & Charcoal Sketch", description: "Creating artwork through traditional pencil and charcoal sketching. Exploring various artistic styles and techniques.", link: "https://www.instagram.com/hakucha_arts/" },
      { name: "3D Printing", description: "Enthusiast of 3D printing technology. Designing and printing creative projects. Follow my work on Instagram.", link: "https://www.instagram.com/atelier.studio.np/" },
      { name: "Coding", description: "Building fun projects and tools for personal use or learning. Passionate about coding as a creative outlet." },
      { name: "Fish Keeping", description: "Maintaining and caring for aquariums. Enjoying the peaceful hobby of fishkeeping and aquatic gardening." },
      { name: "Anime Watching", description: "Avid anime enthusiast. Watching and enjoying various anime series and staying updated with new releases." },
      { name: "Gaming", description: "Love open-world RPG games like Genshin Impact and Wuthering Waves. Exploring immersive game worlds when time permits." }
    ],

    socials: {
      discord: { username: "MR.EIJI", icon: MessageCircle, link: null },
      instagram: [
        { username: "mhrjn_sujan", link: "https://www.instagram.com/mhrjn_sujan/", type: "Photography" },
        { username: "hakucha_arts", link: "https://www.instagram.com/hakucha_arts/", type: "Sketch" },
        { username: "atelier.studio.np", link: "https://www.instagram.com/atelier.studio.np/", type: "3D Printing" }
      ],
      viber: { contact: "+977 9860942721", link: "viber://chat?number=%2B9779860942721", icon: Phone },
      whatsapp: { contact: "+977 9860942721", link: "https://wa.me/9779860942721", icon: MessageCircle },
      github: { username: "sujanmhrjn1301", link: "https://github.com/sujanmhrjn1301", icon: Github },
      linkedin: { username: "Sujan Maharjan", link: "https://www.linkedin.com/in/sujan-maharjan-870b46252/", icon: Linkedin }
    },

    skills: {
      programming: "Python, Node.js, HTML, CSS, JavaScript, React, RAG Systems",
      softSkills: "Collaboration and Communication, Ability to give and receive feedback, Growth Mindset",
      tools: "Airtable, Git/GitHub, Twilio, OpenAI API, Gemini API, Openrouter"
    },

    languages: "Nepali, English"
  };

  return (
    <>
      {/* Blurred Background Overlay */}
      <div
        className="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
        onClick={() => onClose()}
      />

      {/* Modal Container */}
      <div className="fixed inset-0 z-50 flex items-center justify-center p-0 sm:p-4">
        <div className="w-full h-full sm:h-[520px] sm:max-w-2xl bg-[#202123] rounded-none sm:rounded-xl overflow-hidden flex flex-col sm:flex-row shadow-2xl">
          
          {/* Left Sidebar with Tabs - Hidden on mobile, shown on desktop */}
          <div className="hidden sm:flex w-48 bg-[#191919] overflow-y-auto flex-shrink-0 flex-col">
            <div className="flex items-center justify-start px-6 py-5">
              <button
                onClick={() => onClose()}
                className="text-[#ececf1] hover:text-white transition-colors p-1 hover:bg-[#343541] rounded"
              >
                <X size={20} />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full px-4 py-3 text-left transition-all duration-200 text-sm ${
                    activeTab === tab.id
                      ? 'bg-[#343541] text-white'
                      : 'text-[#ececf1] hover:bg-[#232327]'
                  }`}
                >
                  <span className="flex items-center gap-2">
                    {React.createElement(iconMap[tab.id], { size: 18, className: 'text-[#ececf1]' })}
                    {tab.label}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Right Content Area */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Header */}
            <div className="flex items-center justify-center px-4 sm:px-6 py-3 sm:py-5 flex-shrink-0 relative">
              <button
                onClick={() => onClose()}
                className="absolute left-4 sm:hidden text-[#ececf1] hover:text-white transition-colors p-1 hover:bg-[#343541] rounded"
                title="Close"
              >
                <X size={20} />
              </button>
              <div className="flex flex-col items-center w-full">
                <h2 className="text-lg sm:text-xl font-semibold text-white mb-3 sm:mb-4">
                  {tabs.find(t => t.id === activeTab)?.label}
                </h2>
                <div className="w-64 sm:w-80 h-px bg-[#565869]"></div>
              </div>
            </div>

            {/* Content Scrollable Area */}
            <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-4 sm:py-5 space-y-4 sm:space-y-5 pb-20 sm:pb-0">
                {/* Personal Info Tab */}
                {activeTab === 'personal' && (
                  <div className="space-y-5 max-w-2xl">
                    <div>
                      <p className="text-xs font-semibold text-[#d1d5db] uppercase mb-1">Name</p>
                      <p className="text-sm text-[#ececf1]">{cvData.name}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-[#d1d5db] uppercase mb-1">Location</p>
                      <p className="text-sm text-[#ececf1]">{cvData.location}</p>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-[#d1d5db] uppercase mb-1">Email</p>
                      <a href={`mailto:${cvData.email}`} className="text-sm text-blue-500 hover:text-blue-400">{cvData.email}</a>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-[#d1d5db] uppercase mb-1">Phone</p>
                      <a href={`tel:${cvData.phone}`} className="text-sm text-blue-500 hover:text-blue-400">{cvData.phone}</a>
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-[#d1d5db] uppercase mb-1">Bio</p>
                      <p className="text-sm text-[#d1d5db] leading-relaxed">{cvData.bio}</p>
                    </div>
                  </div>
                )}

                {/* Academic Info Tab */}
                {activeTab === 'academic' && (
                  <div className="space-y-5">
                    {cvData.education.map((edu, idx) => (
                      <div key={idx} className="border-b border-[#2d2d3d] pb-5 last:border-b-0">
                        <p className="text-sm font-semibold text-[#ececf1] mb-1">{edu.level}</p>
                        <p className="text-xs text-[#d1d5db] mb-1">{edu.school}</p>
                        <p className="text-xs text-[#9ca3af]">{edu.location} • {edu.period}</p>
                        {edu.gpa && <p className="text-xs text-[#d1d5db] mt-2">📊 {edu.gpa}</p>}
                      </div>
                    ))}
                  </div>
                )}

                {/* Industry Experience Tab */}
                {activeTab === 'experience' && (
                  <div className="space-y-5">
                    {cvData.experience.map((exp, idx) => (
                      <div key={idx} className="border-b border-[#2d2d3d] pb-5 last:border-b-0">
                        <p className="text-sm font-semibold text-[#ececf1] mb-1">{exp.title}</p>
                        <p className="text-xs text-[#d1d5db] mb-2">{exp.company} • {exp.location}</p>
                        <p className="text-xs text-[#9ca3af] mb-3">{exp.period}</p>
                        <ul className="space-y-2">
                          {exp.highlights.map((highlight, i) => (
                            <li key={i} className="text-xs text-[#d1d5db] flex gap-2">
                              <span className="text-[#9ca3af] flex-shrink-0">•</span>
                              <span>{highlight}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                )}

                {/* Projects Tab */}
                {activeTab === 'projects' && (
                  <div className="space-y-5">
                    {projects && projects.length > 0 ? (
                      projects.map((project, idx) => (
                        <div key={idx} className="border-b border-[#2d2d3d] pb-5 last:border-b-0">
                          <p className="text-sm font-semibold text-[#ececf1] mb-1">{project.title}</p>
                          <p className="text-xs text-[#d1d5db] mb-2 line-clamp-3">{project.description}</p>
                          <div className="flex items-center gap-3 text-xs text-[#9ca3af] mb-3">
                            {project.language && <span>📝 {project.language}</span>}
                            {project.stars > 0 && <span>⭐ {project.stars}</span>}
                          </div>
                          <a
                            href={project.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs text-blue-500 hover:text-blue-400 flex items-center gap-1 transition-colors w-fit"
                          >
                            View on GitHub <ExternalLink size={10} />
                          </a>
                        </div>
                      ))
                    ) : (
                      <p className="text-sm text-[#d1d5db]">Loading projects from GitHub...</p>
                    )}
                  </div>
                )}

                {/* Skills Tab */}
                {activeTab === 'skills' && (
                  <div className="space-y-6">
                    <div>
                      <p className="text-xs font-semibold text-[#d1d5db] uppercase mb-3">💻 Programming & Development</p>
                      <div className="flex flex-wrap gap-2">
                        {cvData.skills.programming.split(',').map((skill, idx) => (
                          <span key={idx} className="bg-[#2d2d3d] text-[#d1d5db] px-2 py-1 rounded text-xs border border-[#565869]">
                            {skill.trim()}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="border-t border-[#2d2d3d] pt-5">
                      <p className="text-xs font-semibold text-[#d1d5db] uppercase mb-3">🤝 Soft Skills</p>
                      <div className="flex flex-wrap gap-2">
                        {cvData.skills.softSkills.split(',').map((skill, idx) => (
                          <span key={idx} className="bg-[#2d2d3d] text-[#d1d5db] px-2 py-1 rounded text-xs border border-[#565869]">
                            {skill.trim()}
                          </span>
                        ))}
                      </div>
                    </div>
                    <div className="border-t border-[#2d2d3d] pt-5">
                      <p className="text-xs font-semibold text-[#d1d5db] uppercase mb-3">🛠️ Tools & Platforms</p>
                      <div className="flex flex-wrap gap-2">
                        {cvData.skills.tools.split(',').map((skill, idx) => (
                          <span key={idx} className="bg-[#2d2d3d] text-[#d1d5db] px-2 py-1 rounded text-xs border border-[#565869]">
                            {skill.trim()}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Certifications Tab */}
                {activeTab === 'certifications' && (
                  <div className="space-y-5">
                    {cvData.certifications.map((cert, idx) => (
                      <div key={idx} className="border-b border-[#2d2d3d] pb-5 last:border-b-0 flex justify-between items-start">
                        <div>
                          <p className="text-sm font-semibold text-[#ececf1] mb-1">{cert.title}</p>
                          <p className="text-xs text-[#d1d5db]">{cert.issuer}</p>
                        </div>
                        <span className="text-xs text-[#9ca3af] bg-[#2d2d3d] px-2 py-1 rounded flex-shrink-0">{cert.year}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Hobbies Tab */}
                {activeTab === 'hobbies' && (
                  <div className="space-y-5">
                    {cvData.hobbies.map((hobby, idx) => (
                      <div key={idx} className="border-b border-[#2d2d3d] pb-5 last:border-b-0">
                        <p className="text-sm font-semibold text-[#ececf1] mb-2">{hobby.name}</p>
                        <p className="text-xs text-[#d1d5db] leading-relaxed mb-3">{hobby.description}</p>
                        {hobby.link && (
                          <a
                            href={hobby.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs text-blue-500 hover:text-blue-400 flex items-center gap-1 transition-colors w-fit"
                          >
                            View on Instagram <ExternalLink size={10} />
                          </a>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {/* Social Media Tab */}
                {activeTab === 'socials' && (
                  <div className="flex flex-col gap-6 py-4">
                    {/* Discord */}
                    <div className="flex items-start">
                      <div className="flex flex-col items-center justify-center flex-shrink-0 w-16 h-16 mr-8">
                        <a
                          href="#"
                          className="hover:opacity-80 transition-opacity"
                          title={cvData.socials.discord.username}
                        >
                          <svg width="40" height="40" viewBox="0 0 24 24" fill="currentColor" className="text-[#ececf1]">
                            <path d="M20.317 4.3671C18.7975 3.6368 17.147 3.0979 15.3917 2.8624C15.1525 3.264 14.8785 3.8956 14.6598 4.4062C12.7381 4.0866 10.8212 4.0866 8.9369 4.4062C8.7182 3.8956 8.4362 3.264 8.1969 2.8624C6.4416 3.0979 4.7911 3.637 3.2716 4.3671C0.472697 8.55002 -0.0181808 12.6383 0.141459 16.6984C2.18625 18.1139 4.16857 18.8814 6.11387 19.2459C6.62493 18.4762 7.05403 17.6539 7.39564 16.784C6.61193 16.4897 5.86628 16.163 5.13946 15.7747C5.34715 15.6062 5.54572 15.4276 5.73578 15.2486C9.491 17.1115 13.6383 17.1115 17.3766 15.2486C17.5667 15.4276 17.7652 15.6062 17.9729 15.7747C17.2461 16.163 16.5005 16.4897 15.7168 16.784C16.0584 17.6539 16.4875 18.4762 16.9986 19.2459C18.9429 18.8814 20.9251 18.1139 22.9699 16.6984C23.1876 12.0789 22.4694 8.17508 20.317 4.3671ZM8.02107 14.3098C6.8581 14.3098 5.8831 13.2845 5.8831 12.0171C5.8831 10.8499 6.8581 9.8246 8.02107 9.8246C9.18404 9.8246 10.1591 10.8499 10.1591 12.0171C10.1591 13.2845 9.18404 14.3098 8.02107 14.3098ZM15.9896 14.3098C14.8266 14.3098 13.8516 13.2845 13.8516 12.0171C13.8516 10.8499 14.8266 9.8246 15.9896 9.8246C17.1525 9.8246 18.1276 10.8499 18.1276 12.0171C18.1276 13.2845 17.1525 14.3098 15.9896 14.3098Z" />
                          </svg>
                        </a>
                        <p className="text-xs text-[#9ca3af] mt-2">Discord</p>
                      </div>
                      <div className="flex flex-col justify-start ml-4 pt-0.5">
                        <p className="text-xs font-bold text-[#ececf1]">{cvData.socials.discord.username}</p>
                        <p className="text-xs text-[#9ca3af]">Gaming & Community</p>
                      </div>
                    </div>

                    {/* Instagram Accounts */}
                    {cvData.socials.instagram.map((account, idx) => (
                      <div key={idx} className="flex items-start">
                        <div className="flex flex-col items-center justify-center flex-shrink-0 w-16 h-16 mr-8">
                          <a
                            href={account.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="hover:opacity-80 transition-opacity"
                            title={account.username}
                          >
                            <Instagram size={40} className="text-[#ececf1]" />
                          </a>
                          <p className="text-xs text-[#9ca3af] mt-2">Instagram</p>
                        </div>
                        <div className="flex flex-col justify-start ml-4 pt-0.5">
                          <a
                            href={account.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-xs font-bold text-[#d1d5db] hover:text-[#ececf1] transition-colors flex items-center gap-1"
                          >
                            {account.username}
                            <ExternalLink size={12} />
                          </a>
                          <p className="text-xs text-[#9ca3af]">{account.type}</p>
                        </div>
                      </div>
                    ))}

                    {/* Viber */}
                    <div className="flex items-start">
                      <div className="flex flex-col items-center justify-center flex-shrink-0 w-16 h-16 mr-8">
                        <a
                          href={cvData.socials.viber.link}
                          className="hover:opacity-80 transition-opacity"
                          title="Viber"
                        >
                          <img src={viberIcon} alt="Viber" width="40" height="40" style={{ filter: 'invert(1)' }} />
                        </a>
                        <p className="text-xs text-[#9ca3af] mt-2">Viber</p>
                      </div>
                      <div className="flex flex-col justify-start ml-4 pt-0">
                        <a
                          href={cvData.socials.viber.link}
                          className="text-xs font-bold text-[#d1d5db] hover:text-[#ececf1] transition-colors flex items-center gap-1"
                        >
                          {cvData.socials.viber.contact}
                          <ExternalLink size={12} />
                        </a>
                        <p className="text-xs text-[#9ca3af]">Chat & Call</p>
                      </div>
                    </div>

                    {/* WhatsApp */}
                    <div className="flex items-start">
                      <div className="flex flex-col items-center justify-center flex-shrink-0 w-16 h-16 mr-8">
                        <a
                          href={cvData.socials.whatsapp.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="hover:opacity-80 transition-opacity"
                          title="WhatsApp"
                        >
                          <img src={whatsappIcon} alt="WhatsApp" width="40" height="40" style={{ filter: 'invert(1)' }} />
                        </a>
                        <p className="text-xs text-[#9ca3af] mt-2">WhatsApp</p>
                      </div>
                      <div className="flex flex-col justify-start ml-4 pt-0.5">
                        <a
                          href={cvData.socials.whatsapp.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs font-bold text-[#d1d5db] hover:text-[#ececf1] transition-colors flex items-center gap-1"
                        >
                          {cvData.socials.whatsapp.contact}
                          <ExternalLink size={12} />
                        </a>
                        <p className="text-xs text-[#9ca3af]">Chat & Call</p>
                      </div>
                    </div>

                    {/* GitHub */}
                    <div className="flex items-start">
                      <div className="flex flex-col items-center justify-center flex-shrink-0 w-16 h-16 mr-8">
                        <a
                          href={cvData.socials.github.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="hover:opacity-80 transition-opacity"
                          title="GitHub"
                        >
                          <Github size={40} className="text-[#ececf1]" />
                        </a>
                        <p className="text-xs text-[#9ca3af] mt-2">GitHub</p>
                      </div>
                      <div className="flex flex-col justify-start ml-4 pt-0.5">
                        <a
                          href={cvData.socials.github.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs font-bold text-[#d1d5db] hover:text-[#ececf1] transition-colors flex items-center gap-1"
                        >
                          {cvData.socials.github.username}
                          <ExternalLink size={12} />
                        </a>
                        <p className="text-xs text-[#9ca3af]">Code & Projects</p>
                      </div>
                    </div>

                    {/* LinkedIn */}
                    <div className="flex items-start">
                      <div className="flex flex-col items-center justify-center flex-shrink-0 w-16 h-16 mr-8">
                        <a
                          href={cvData.socials.linkedin.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="hover:opacity-80 transition-opacity"
                          title="LinkedIn"
                        >
                          <Linkedin size={40} className="text-[#ececf1]" />
                        </a>
                        <p className="text-xs text-[#9ca3af] mt-2">LinkedIn</p>
                      </div>
                      <div className="flex flex-col justify-start ml-4 pt-0.5">
                        <a
                          href={cvData.socials.linkedin.link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs font-bold text-[#d1d5db] hover:text-[#ececf1] transition-colors flex items-center gap-1"
                        >
                          {cvData.socials.linkedin.username}
                          <ExternalLink size={12} />
                        </a>
                        <p className="text-xs text-[#9ca3af]">Professional</p>
                      </div>
                    </div>
                  </div>
                )}
            </div>

            {/* Mobile Tab Navigation - Shown only on mobile */}
            <div className="flex sm:hidden w-full bg-[#191919] border-t border-[#2d2d3d] overflow-x-auto flex-shrink-0">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 min-w-max px-3 py-3 text-center transition-all duration-200 text-xs border-b-2 ${
                    activeTab === tab.id
                      ? 'bg-[#2d2d3d] text-white border-b-blue-400'
                      : 'text-[#ececf1] border-b-transparent hover:bg-[#232327]'
                  }`}
                  title={tab.label}
                >
                  {React.createElement(iconMap[tab.id], { size: 16, className: 'inline mr-1' })}
                  <span className="hidden sm:inline">{tab.label}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Profile;
