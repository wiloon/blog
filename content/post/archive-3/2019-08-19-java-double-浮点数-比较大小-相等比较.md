---
title: 'Java Double 浮点数 比较大小 & 相等比较'
author: wiloon
type: post
date: 2019-08-19T07:31:09+00:00
url: /?p=14814
categories:
  - Uncategorized

---
<pre><code class="language-java line-numbers">public class DoubleUtils {
    private static final double DEFAULT_DELTA = 0.000001; //默认比较精度

    //比较2个double值是否相等（默认精度）
    public static boolean considerEqual(double v1, double v2) {
        return considerEqual(v1, v2, DEFAULT_DELTA);
    }

    //比较2个double值是否相等（指定精度）
    public static boolean considerEqual(double v1, double v2, double delta) {
        return Double.compare(v1, v2) == 0 || considerZero(v1 - v2, delta);
    }

    //判断指定double是否为0（默认精度）
    public static boolean considerZero(double value) {
        return considerZero(value, DEFAULT_DELTA);
    }

    //判断指定double是否为0（指定精度）
    public static boolean considerZero(double value, double delta) {
        return Math.abs(value) &lt;= delta;
    }

    /**
     * @param v1 v1
     * @param v2 v2
     * @return result
     * v1&gt;v2, result = 1
     * v1=v2, result =0
     * v1&lt;v2, result =-1
     */
    public static int compare(double v1, double v2) {
        if (v1 - v2 &gt; DEFAULT_DELTA) {
            return 1;
        } else if (considerEqual(v1, v2)) {
            return 0;
        } else {
            return -1;
        }
    }
}

</code></pre>

https://blog.csdn.net/z69183787/article/details/81318486