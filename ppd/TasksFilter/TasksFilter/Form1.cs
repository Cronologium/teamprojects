using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Runtime.InteropServices;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TasksFilter
{
    public partial class Form1 : Form
    {
        private Bitmap blurredBmap;
        Int64[,,] colors;

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            label1.Text = "BlurSize: " + trackBar1.Value * 2;
            textBox1.Text = "8";
        }

        private void Blur(Image image, Rectangle rectangle, Int32 blurSize, Int32 threads)
        {
            // make an exact copy of the bitmap provided
            using (Graphics graphics = Graphics.FromImage(blurredBmap))
                graphics.DrawImage(image, new Rectangle(0, 0, image.Width, image.Height),
                    new Rectangle(0, 0, image.Width, image.Height), GraphicsUnit.Pixel);
            colors = new Int64[image.Width + 1, image.Height + 1, 3];

            var data = blurredBmap.LockBits(rectangle, ImageLockMode.ReadWrite, blurredBmap.PixelFormat);
            var depth = Bitmap.GetPixelFormatSize(data.PixelFormat) / 8; //bytes per pixel

            var buffer = new byte[data.Width * data.Height * depth];

            //copy pixels to buffer
            Marshal.Copy(data.Scan0, buffer, 0, buffer.Length);

            List<Tuple<Int32, Int32>> yCoordinates = new List<Tuple<Int32, Int32>>();
            Int32 widthPerThread = image.Width / threads;
            for (Int32 i = 0; i * widthPerThread < image.Width; ++i)
            {
                if (i == 0)
                    yCoordinates.Add(new Tuple<int, int>(0, (i + 1) * widthPerThread));
                else
                {
                    Tuple<Int32, Int32> prev = yCoordinates[i - 1];
                    Int32 lower = prev.Item2 + 1;
                    Int32 higher = lower + widthPerThread - 1;
                    yCoordinates.Add(new Tuple<int, int>(lower, higher));
                }
            }

            Task[] tasks = new Task[yCoordinates.Count];
            int j = 0;
            Int32 maxHeight = image.Height;
            Int32 maxWidth = image.Width;
            System.Diagnostics.Debug.WriteLine(maxWidth);
            foreach (var interval in yCoordinates)
            {
                tasks[j] = new Task(() => Process(buffer, interval.Item1, 0, interval.Item2, maxHeight, data.Width, depth, blurSize, maxWidth, maxHeight));
                j++;
            }

            foreach (Task t in tasks)
            {
                t.Start();
                //t.Wait();
            }

            Task.WaitAll(tasks);

            //Copy the buffer back to image
            Marshal.Copy(buffer, 0, data.Scan0, buffer.Length);

            blurredBmap.UnlockBits(data);
        }

        private void Process(byte[] buffer, Int32 x, Int32 y, Int32 endx, Int32 endy, Int32 width, Int32 depth, Int32 blurSize, Int32 maxWidth, Int32 maxHeight)
        {
            Int32 range = blurSize / 2;
            Int32 totalPixelsModified = 0;
            for (int i = x; i <= endx; i++)
            {
                for (int j = y; j <= endy; j++)
                {
                    Int64 avgR = 0, avgB = 0, avgG = 0, count = 0;

                    for (int ii = Math.Max(i - range, 0); ii <= i + range && ii < maxWidth; ++ii)
                    {
                        for (int jj = Math.Max(j - range, 0); jj <= j + range && jj < maxHeight; ++jj)
                        {
                            var offset = ((jj * width) + ii) * depth;
                            avgR += buffer[offset + 0];
                            avgB += buffer[offset + 1];
                            avgG += buffer[offset + 2];

                            count++;
                        }
                    }

                    if (count > 0)
                    {
                        avgR /= count;
                        avgB /= count;
                        avgG /= count;
                    }

                    for (int ii = Math.Max(i - range, 0); ii <= i + range && ii < maxWidth; ++ii)
                    {
                        for (int jj = Math.Max(j - range, 0); jj <= j + range && jj < maxHeight; ++jj)
                        {
                            var offset = ((jj * width) + ii) * depth;
                            buffer[offset + 0] = (byte)avgR;
                            buffer[offset + 1] = (byte)avgB;
                            buffer[offset + 2] = (byte)avgG;
                            totalPixelsModified++;
                        }
                    }
                }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            pictureBox1.Image = Properties.Resources.test;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Int32 threads = Int32.Parse(textBox1.Text);
            blurredBmap = new Bitmap(Properties.Resources.test.Width, Properties.Resources.test.Height);
            Blur(Properties.Resources.test, new Rectangle(0, 0, blurredBmap.Width, blurredBmap.Height), trackBar1.Value * 2, threads);
            pictureBox1.Image = blurredBmap;
        }

        private void trackBar1_Scroll(object sender, EventArgs e)
        {
            label1.Text = "BlurSize: " + trackBar1.Value * 2;
        }
    }
}
